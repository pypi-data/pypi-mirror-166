# coding: utf-8
"""The mod:`piaf.api.routes` modules defines all routes available in the Web API."""
from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

import async_timeout as at
from fastapi import APIRouter, Response, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse

from piaf.agent import AgentState
from piaf.api.managers import ptf_manager
from piaf.api.models import (
    ACLMessageModel,
    AgentCreationDescriptionModelIn,
    AgentPlatformModelIn,
    AgentStateModel,
    AIDModel,
    AMSAgentDescriptionModelOut,
    ExceptionModel,
)
from piaf.events import Topic

if TYPE_CHECKING:
    from aioredis.client import PubSub

# V1 router
app_v1 = APIRouter()


@app_v1.post(
    "/platforms",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel},
    },
)
async def create_platform(ptf: AgentPlatformModelIn, response: Response):
    """
    Create a new AgentPlatform with the provided name.

    :param ptf: the platform description
    """
    try:
        await ptf_manager.spawn(ptf)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"details": str(e)}


@app_v1.delete(
    "/platforms/{name}",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel},
    },
)
async def delete_platform(name: str, response: Response):
    """
    Stop and delete the desired platform.

    :param ptf: the platform's name
    :param response: injected response by FastAPI
    """
    try:
        try:
            await ptf_manager.stop(name)
        except asyncio.TimeoutError:
            await ptf_manager.kill(name)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"details": str(e)}


@app_v1.get("/platforms", response_model=List[AgentPlatformModelIn])
async def get_platforms():
    """Get all the running platforms this application is aware of."""
    return await ptf_manager.get_all_platforms()


@app_v1.post(
    "/platforms/{name}/agents",
    status_code=status.HTTP_200_OK,
    response_model=AIDModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel},
    },
)
async def create_agent(name: str, agent: AgentCreationDescriptionModelIn):
    """
    Create and invoke an agent into the specified platform.

    :param name: the platform's name
    :param agent: the description of the agent to create
    :return: an positive reply containing the AID of the created agent or the description o the error
    """
    task = {"task_type": "CreateAgentTask", "id": str(uuid4())}
    task.update(agent.dict())
    return await process_task(name, task)


@app_v1.get(
    "/platforms/{ptf_name}/agents",
    status_code=status.HTTP_200_OK,
    response_model=List[AMSAgentDescriptionModelOut],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel},
    },
)
async def get_agents(
    ptf_name: str,
    state: Optional[AgentState] = None,
    name: str = "",
):
    """
    Retrieve for the given platform all the agents matching the criteria.

    :param ptf_name: the name of the platform
    :param state: (Optional, default to ALL) only take the agents in the given state
    :param name: (Optional, default to "") filter agents to retain only the ones having the given string given in their shortname.
    :return: either a list of agent description or an error message
    """
    task = {
        "task_type": "GetAgentsTask",
        "filters": {"state": state.name if state is not None else None, "name": name},
        "id": str(uuid4()),
    }
    return await process_task(ptf_name, task)


@app_v1.delete(
    "/platforms/{ptf_name}/agents/{name}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel}},
)
async def delete_agent(ptf_name: str, name: str):
    """
    Delete an agent from the given platform.

    :param ptf_name: the name of the platform
    :param name: the agent's shortname
    """
    task = {
        "task_type": "ChangeAgentStateTask",
        "name": name,
        "state": "UNKNOWN",
        "id": str(uuid4()),
    }
    return await process_task(ptf_name, task)


@app_v1.get(
    "/platforms/{ptf_name}/agents/{name}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel}},
)
async def get_agent_memory(ptf_name: str, name: str):
    """
    Get a snapshot of the current agent's memory.

    :param ptf_name: name of the platform where the agent live
    :param name: shortname of the agent
    """
    task = {
        "task_type": "RetrieveAgentMemoryTask",
        "aid": {"name": f"{name}@{ptf_name}"},
        "id": str(uuid4()),
    }
    return await process_task(ptf_name, task)


@app_v1.post(
    "/platforms/{ptf_name}/agents/{name}/messages",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel}},
)
async def send_message(ptf_name: str, name: str, msg: ACLMessageModel):
    """
    Send a message on the behalf of a specific agent.

    :param ptf_name: name of te platform
    :param name: name of the agent
    :param msg: the message to send
    """
    task = {
        "task_type": "SendMessageTask",
        "id": str(uuid4()),
        "msg": json.loads(msg.json()),
        "sender": f"{name}@{ptf_name}",
    }
    return await process_task(ptf_name, task)


@app_v1.put(
    "/platforms/{ptf_name}/agents/{name}/state",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionModel},
    },
)
async def update_agent_state(ptf_name: str, name: str, state: AgentStateModel):
    """
    Replace an agent's state by the provided one.

    :param ptf_name: the name of the platform where the agent live
    :param name: shortname of the agent
    :param state: the new state
    """
    task = {
        "task_type": "ChangeAgentStateTask",
        "name": name,
        "state": state.state.name,
        "id": str(uuid4()),
    }
    return await process_task(ptf_name, task)


@app_v1.websocket("/platforms/{ptf_name}/ws")
async def topic_listener(ptf_name: str, websocket: WebSocket) -> None:
    """
    Get a websocket that can listen on the platform's event.

    The websocket supports two methods:

    - subscribe: subscribe to a particular topic
    - unsubscribe: unsubscribe from a particular topic

    Here is the Json object::

        {
            method: "[un]subscribe",
            topic: ".some.topic"
        }

    .. warning:: Contrary to how events are dispatched inside the piaf platform, events are not dispatched to topic's parents. It means that listening on `.platform` won't catch events emitted on `.platform.agents` for example.

    :param ptf_name: the platform's name
    :param websocket: injected by FastAPI
    """

    try:
        await websocket.accept()
        pubsub: PubSub = ptf_manager.db.pubsub()
        first_sub: bool = True

        while True:
            try:
                data: Dict[str, Any] = await websocket.receive_json()
            except WebSocketDisconnect:
                break

            topic = Topic.from_str(data["topic"])
            if data["method"] == "subscribe":
                await pubsub.subscribe(f"channels:{ptf_name}:events:{topic}")

            if data["method"] == "unsubscribe":
                await pubsub.unsubscribe(f"channels:{ptf_name}:events:{topic}")

            if first_sub:
                task = asyncio.create_task(yield_events(pubsub, websocket))
                first_sub = False
    finally:
        task.cancel()
        await pubsub.close()


async def yield_events(pubsub: PubSub, ws: WebSocket) -> None:
    """
    Asynchronous task that keeps listening on the provided pubsub and yielding downloaded data to the provided websocket.

    :param pubsub: redis publish/subscribe object
    :param ws: websocket
    """
    while True:
        record = await pubsub.get_message(ignore_subscribe_messages=True, timeout=2)
        if record is not None:
            await ws.send_json(json.loads(record["data"]))
        await asyncio.sleep(0)


async def process_task(
    ptf_name: str, task: Dict[str, Any], timeout: float = 5
) -> JSONResponse:
    """
    Send the given task to the APIAgent in the specified platform.

    If the platform doesn't exists, then returns an HTTP 404 response. Otherwise the task is submitted to the platform and the result is returned.

    :param ptf_name: name of the platform
    :param task: a JSON-compatible dict describing the task to submit
    :param timeout: time (in seconds) given to the task for its execution
    :return: a :class:`JSONRequest` with the result or the error.
    """
    # Ensure platform exists
    platforms = await ptf_manager.get_all_platforms()
    if ptf_name not in (ptf["name"] for ptf in platforms):
        return JSONResponse(
            content={"details": f"Unknown platform '{ptf_name}'"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Subscribe
    pubsub = ptf_manager.db.pubsub(ignore_subscribe_messages=True)
    await pubsub.subscribe(f"channels:{ptf_name}:to-api")

    # Wait for reply
    try:
        async with at.timeout(timeout):

            # Send task here (retry until delivered to the API agent or timeout)
            while (
                await ptf_manager.db.publish(
                    f"channels:{ptf_name}:from-api", json.dumps(task)
                )
                == 0
            ):
                await asyncio.sleep(0.1)

            # Await response
            async for msg in pubsub.listen():
                reply = json.loads(msg["data"])
                if reply["id"] == task["id"]:
                    break
    finally:
        await pubsub.close()

    # Return result as a valid response
    if reply["error"] is not None:
        return JSONResponse({"details": reply["error"]}, status.HTTP_400_BAD_REQUEST)
    return JSONResponse(reply["data"])
