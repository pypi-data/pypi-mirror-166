# coding: utf-8
""" This module contains a set of helper objects."""
from __future__ import annotations

import asyncio
import importlib
import json
import os
import signal
from enum import Enum
from multiprocessing import Process
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Union
from uuid import uuid4

import aioredis
import async_timeout as at

from piaf.agent import Agent
from piaf.api.models import AgentPlatformModelIn
from piaf.behavior import Behavior, FSMBehavior
from piaf.comm import AID, ACLMessage
from piaf.events import Event, EventRecord, Subscriber, Topic
from piaf.launcher import PlatformLauncher, ServiceDescription
from piaf.ptf import AgentPlatformFacade
from piaf.service import AMSAgentDescription

if TYPE_CHECKING:
    from aioredis import Redis
    from aioredis.client import PubSub


class PlatformManager:
    """
    The :class:`PlatformManager`  class contains the necessary tools to spawn, kill and communicate with running platforms.

    It also manages a connection to the Redis database.
    """

    PLATFORMS_REDIS_SET = "platforms"
    PLATFORM_PREFIX_HASHSET = "platform:"

    def __init__(self) -> None:
        """Create the platform manager with no connection established yet."""
        self._db = None

    @property
    def db(self) -> aioredis.Redis:
        """
        Get the Redis connection.

        :raise Exception: the :class:`PlatformManager` object is not initialized
        :return: the database connection
        """
        if self._db is None:
            raise Exception("Database connection is not initialized.")
        return self._db

    async def initialize(self) -> None:
        """Initialize the :class:`PlatformManager` and establish a connection with the Redis database."""
        self._db = await aioredis.from_url(
            "redis://localhost:6379",  # TODO: move in a configuration variable
            decode_responses=True,
        )

    async def spawn(self, ptf: AgentPlatformModelIn, timeout: float = 2) -> None:
        """
        Try to spawn a new platform.

        :param ptf: the platform description supplied by the user
        :param timeout: how much time to wait the creation of the platform
        :raise Exception: the supplied platform's name is already taken or timeout is reached
        """
        if await self.db.sismember(self.PLATFORMS_REDIS_SET, ptf.name):
            raise Exception(f"Duplicated platform name {ptf.name}")

        # Subscribe to events coming from the future platform
        pubsub: PubSub = self.db.pubsub(ignore_subscribe_messages=True)
        await pubsub.subscribe(f"channels:{ptf.name}:events:.platform.agents.api")

        # Launch the platform
        info = self._spawn_process(ptf)

        # Wait until the platform is ready (ie the APIAgent is up)
        try:
            async with at.timeout(timeout):
                async for msg in pubsub.listen():
                    record: Dict[str, Any] = json.loads(msg["data"])
                    if record["event"]["type"] == "agent_creation":
                        break
        finally:
            await pubsub.close()

        # Store information about the platform in the redis database
        await self.db.sadd(self.PLATFORMS_REDIS_SET, ptf.name)
        await self.db.hset(self.PLATFORM_PREFIX_HASHSET + ptf.name, mapping=info)

    def _spawn_process(self, ptf: AgentPlatformModelIn) -> Dict[str, Any]:
        """
        Spawn a new agent platform as a process.

        :param ptf: description of the platform to create
        :return: a mapping describing the platform : the name, the type (process) and the process's pid
        """
        process = _AgentPlatformProcess(ptf.name)
        process.start()

        return {"type": "process", "name": ptf.name, "pid": process.pid}

    def _spawn_docker(self, ptf: AgentPlatformModelIn) -> Dict[str, Any]:
        """
        Spawn a new agent platform as a docker container.

        :param ptf: description of the platform to create
        :return: a mapping describing the platform : the name, the type (docker) and the container's hash
        """
        raise NotImplementedError()

    async def stop(self, name: str, timeout: float = 2) -> None:
        """
        Stop and delete the platform identified by the provided description.

        :param name: the platform's name
        :param timeout: how much time is given to the platform to realize a stop before killing the process
        :raise Exception: there is no platform matching the provided description or timeout is reached
        """
        if not (await self.db.sismember(self.PLATFORMS_REDIS_SET, name)):
            raise Exception(f"Unknown platform {name}")

        # Subscribe to platform events
        pubsub: PubSub = self.db.pubsub(ignore_subscribe_messages=True)
        await pubsub.subscribe(f"channels:{name}:events:.platform")

        # Publish the task to stop the platform
        await self.db.publish(
            f"channels:{name}:from-api",
            json.dumps({"task_type": "StopPlatformTask", "id": str(uuid4())}),
        )

        # Wait until a 'platform-death' event is received or timeout is reached
        try:
            async with at.timeout(timeout):
                async for msg in pubsub.listen():
                    record: Dict[str, Any] = json.loads(msg["data"])
                    if (
                        record["event"]["type"] == "state_change"
                        and record["event"]["data"]["to"] == "STOPPED"
                    ):
                        break
        finally:
            await pubsub.close()

        # Delete record from database
        record = await self.db.hgetall(self.PLATFORM_PREFIX_HASHSET + name)
        await self.db.delete(self.PLATFORM_PREFIX_HASHSET + name)
        await self.db.srem(self.PLATFORMS_REDIS_SET, name)

    async def kill(self, name: str) -> None:
        """
        Kill the provided platform without letting it finishing properly.

        :param name: name of the platform
        :raise Exception: there is no platform matching the provided description
        """
        if not (await self.db.sismember(self.PLATFORMS_REDIS_SET, name)):
            raise Exception(f"Unknown platform {name}")

        # Get the platform's description
        record: Dict[str, Any] = await self.db.hgetall(
            self.PLATFORM_PREFIX_HASHSET + name
        )
        if record["type"] == "process":
            await self._kill_process(record)
        else:
            await self._kill_docker(record)

        # Delete record from database
        await self.db.delete(self.PLATFORM_PREFIX_HASHSET + name)
        await self.db.srem(self.PLATFORMS_REDIS_SET, name)

    async def _kill_process(self, description: Dict[str, Any]) -> None:
        """
        Kill a platform running in a dedicated process.

        :param description: description of the platform to kill. It should contain a 'type' entry set to 'process' and a 'pid' entry set to the process's pid.
        """
        os.kill(int(description["pid"]), signal.SIGTERM)

    async def _kill_docker(self, description: Dict[str, Any]) -> None:
        """
        Kill a platform running in a docker container.

        :param description: description of the platform to kill. It should contain a 'type' entry set
        to 'docker' and a 'hash' entry set to the container's hash.
        """
        raise NotImplementedError()

    async def get_all_platforms(self) -> List[Mapping[str, str]]:
        """
        Interrogate the Redis database to get all the running platforms.

        :return: a list of platform names
        """
        records = await self.db.smembers(self.PLATFORMS_REDIS_SET)
        return [{"name": ptf} for ptf in records]


# A global instance
ptf_manager = PlatformManager()


class _AgentPlatformProcess(Process):
    """A customized process that runs a :class:`piaf.ptf.AgentPlatform` on a local asynchronous loop."""

    def __init__(self, name: str) -> None:
        """
        Create a new instance.

        :param name: name of the platform, which will also be the name of the thread.
        """
        super().__init__(name=name, daemon=True)

    def run(self) -> None:
        """
        Create the asynchronous loop and launch the platform.

        The platform will start with an agent called 'api', which can receive tasks
        from a web interface to execute. For now, logs are streamed in the parent's
        console (if any).
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        import logging

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("{processName} - {levelname:<8}:{message}", style="{")
        )
        logger.addHandler(handler)

        REDIS_URL = "redis://localhost:6379"  # TODO: move in a configuration variable
        self.launcher = PlatformLauncher(self.name)
        self.launcher.add_service(
            ServiceDescription("api", APIAgent, kwargs={"redis_url": REDIS_URL})
        )

        async def redis():
            db: Redis = await aioredis.from_url(REDIS_URL, decode_responses=True)  # type: ignore
            self.launcher.ptf.evt_manager.subscribe_to(
                EventsToRedis(self.name, db),  # type: ignore
                Topic.from_str(""),
            )

        self.loop.create_task(redis())
        self.launcher.run()


class APIAgent(Agent):
    """
    A special agent that can communicate with the web API through a Redis connection.

    The agent will first try to connect to the redis database and then will listen to incoming tasks. Tasks execution results are sent back to the web API.
    """

    def __init__(self, aid: AID, platform: AgentPlatformFacade, redis_url: str):
        """
        Initialize a new :class:`APIAgent` instance.

        :param aid: the agent's :class:`AID`
        :param platform: a reference to the underlying platform
        :param redis_url: the url to the redis database
        """
        super().__init__(aid, platform)
        self.db: Redis | None = None
        self.channel: PubSub | None = None

        fsm = FSMBehavior(self)
        fsm.add_state("START", ConnectToRedisBehavior, kwargs={"redis_url": redis_url})
        fsm.add_state("RUN", ExecuteTasksBehavior, final=True)
        fsm.set_initial_state("START")

        fsm.add_transition("START", "RUN", lambda e: True)

        self.add_behavior(fsm)


class ConnectToRedisBehavior(Behavior):
    """
    A behavior that establishes a connection to a redis database and stores that connection into the agent.

    In addition, it also creates a :class:`aioredis.PubSub` object (channel) subscribing to the incoming tasks queue.
    """

    def __init__(self, agent: APIAgent, redis_url: str):
        """
        Initialize a new :class:`ConnectToRedisBehavior`.

        :param agent: the behavior's owner
        :param redis_url: the url to the redis database
        """
        super().__init__(agent)
        self.redis_url = redis_url

    async def action(self) -> None:
        """
        Establish a connection with the redis database and create a channel.

        Both object are stored in the owner. The channel subscribes to the incoming tasks queue for the current platform.
        """
        self.agent.db = await aioredis.from_url(self.redis_url, decode_responses=True)  # type: ignore
        self.agent.channel = self.agent.db.pubsub(ignore_subscribe_messages=True)  # type: ignore
        await self.agent.channel.subscribe(  # type: ignore
            f"channels:{self.agent.aid.hap_name}:from-api"
        )

    def done(self) -> bool:
        """
        One shot behavior, always return `True`.

        :return: `True`
        """
        return True


class ExecuteTasksBehavior(Behavior):
    """
    Pull tasks from the redis channel and execute each one sequentially.

    This behavior requires an open connection to the redis database and a channel listening on the input tasks queue.
    """

    def __init__(self, agent: APIAgent):
        """
        Initialize a new :class:`ExecuteTasksBehavior` instance.

        :param agent: the owner
        """
        super().__init__(agent)

    async def action(self) -> None:
        """
        Wait for incoming tasks and execute each one sequentially.

        Incoming tasks should have the following structure::

            {
                "task_type": "[module.]class",
                "id": "id_of_the_task",
                ...
            }

        Tasks' class are dynamically imported from the specified module or :mod:`piaf.api.tasks` if no module is specified. Results are sent back in json into the response queue. The structure of a response is the following::

            {
                "id": "id-of-the-request",
                "data": whatever is returned by the task's execution or null,
                "error": error message if the execution failed, null otherwise
            }


        """
        async for task in self.agent.channel.listen():  # type: ignore
            json_task: Dict[str, Any] = json.loads(task["data"])
            data = json_task["task_type"]
            split_data = data.rsplit(".", maxsplit=1)

            if len(split_data) == 1:
                module_name = "piaf.api.tasks"
                klass_name = split_data[0]
            else:
                module_name, klass_name = split_data
            module = importlib.import_module(module_name)

            try:
                klass = getattr(module, klass_name)
                id_ = json_task["id"]
                result = await klass.from_json(json_task).execute(self.agent)

                data = json.dumps(
                    {"id": id_, "data": result, "error": None},
                    default=serialize_piaf_object,
                )

                await self.agent.db.publish(  # type: ignore
                    f"channels:{self.agent.aid.hap_name}:to-api",
                    data,
                )

            except Exception as e:
                self.agent.logger.exception("Unable to run task.", exc_info=e)
                await self.agent.db.publish(  # type: ignore
                    f"channels:{self.agent.aid.hap_name}:to-api",
                    json.dumps({"id": id_, "data": None, "error": str(e)}),
                )

    def done(self) -> bool:
        """
        Infinite behavior, always return `True`.

        :return: `True`
        """
        return True


class EventsToRedis(Subscriber):
    """Subscribe to all events and send them into the redis database."""

    def __init__(self, hap_name: str, redis: Redis) -> None:
        super().__init__()
        self.hap_name = hap_name
        self.redis = redis

    async def on_event(self, event_record: EventRecord) -> None:
        """
        Re-publish the event on each queue it is published.

        :param event_record: the record
        """
        json_record = json.dumps(event_record, default=serialize_piaf_object)
        tasks = []
        for channel in event_record.topics:
            tasks.append(
                self.redis.publish(
                    f"channels:{self.hap_name}:events:{channel}", json_record
                )
            )

        results = await asyncio.gather(
            *tasks, return_exceptions=True
        )  # fixme: ignored for now

    async def close(self):
        """
        Close this subscriber.

        It releases the associated Redis connection properly.
        """
        await self.redis.close()


#: A type that represents all JSON-compatible types
JSONType = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]


def serialize_piaf_object(
    o: Any,
) -> JSONType:
    """
    Given a `piaf` object, convert it into a JSON-compatible object.

    :param o: the piaf object to serialize
    :return: a JSON-compatible object
    :raise TypeError: the object can't be serialized
    """
    if isinstance(o, AID):
        return {
            "name": o.name,
            "shortname": o.short_name,
            "addresses": o.addresses,
            "resolvers": [serialize_piaf_object(r) for r in o.resolvers],
        }
    if isinstance(o, Enum):
        return o.name
    if isinstance(o, AMSAgentDescription):
        return {
            "aid": serialize_piaf_object(o.name),
            "state": serialize_piaf_object(o.state),
            "owner": o.ownership,
        }
    if isinstance(o, EventRecord):
        return {
            "event": serialize_piaf_object(o.event),
            "topic": [serialize_piaf_object(topic) for topic in o.topics],
            "timestamp": o.timestamp,
        }
    if isinstance(o, Event):
        return {
            "source": o.source,
            "type": o.type,
            "data": json.loads(json.dumps(o.data, default=serialize_piaf_object)),
        }
    if isinstance(o, Topic):
        return str(o)
    if isinstance(o, ACLMessage):
        return {
            k: json.loads(json.dumps(v, default=serialize_piaf_object))
            for k, v in o.__dict__.items()
        }
    return f"Unserializable object: {type(o)}"
