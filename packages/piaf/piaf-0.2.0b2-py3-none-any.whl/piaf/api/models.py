# coding: utf-8
"""
The :mod:`piaf.api.models` contains all `pydantic` models used to describe input and output data.

Every input models finish with the `In` suffix, while output models finish with the `Out` suffix.
"""
from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, validator

from piaf.agent import AgentState
from piaf.comm import Performative


class AgentPlatformModelIn(BaseModel):
    """
    Describe an incoming agent platform.

    It only contains one field named 'name', witch represents the platform's name to create.
    """

    name: str


class AgentCreationDescriptionModelIn(BaseModel):
    """
    Describe an incoming agent description.

    It should be supplied by the user in order to create an invoke an agent into a platform. The model contains four fields:

    - class_name: the fully qualified name of the agent's type
    - agent_name: the shortname of the agent to create
    - args: Optional, a sequence of arguments used to instantiate the agent
    - is_service: Default `True`, tells if the agent has a full access to the platform
    """

    class_name: str
    agent_name: str
    args: Optional[List[Any]] = None
    is_service: bool = True


class AIDModel(BaseModel):
    """
    Describe an agent identifier.

    The model contains four fields:

    - name: the full name of the agent, including the platform's name
    - shortname: the local name of the agent
    - addresses: a list of addresses used to reach the agent
    - resolvers: a list of naming resolvers
    """

    name: str
    shortname: str
    addresses: List[str] = []
    resolvers: List[AIDModel] = []


AIDModel.update_forward_refs()


class AMSAgentDescriptionModelOut(BaseModel):
    """
    Describe an agent when requested using the AMS.

    The model contains three fields:

    - aid: the agent's identifier
    - state: the state of the agent
    - owner: an optional owner of the agent
    """

    aid: AIDModel
    state: str
    owner: Optional[str]


class ExceptionModel(BaseModel):
    """
    Describe an internal error to give clues about what went wrong.

    The model contains one field named `details`, which describes the error.
    """

    details: str


class AgentStateModel(BaseModel):
    """
    Describe the state of an agent.

    It contains one field named `state` which must be either ACTIVE or SUSPENDED.
    """

    state: AgentState

    @validator("state")
    def restrict_state_values(cls, v):
        """
        Ensure the given value is either `AgentState.ACTIVE` or `AgentState.SUSPENDED`.

        :param cls: model class
        :param v: the value of the 'state' field
        :return: `v` if the value is valid
        :raise ValueError: v is not valid
        """
        if v not in (AgentState.ACTIVE, AgentState.SUSPENDED):
            raise ValueError("Must be either ACTIVE or SUSPENDED")
        return v


class ACLMessageModel(BaseModel):
    """
    Describe an ACLMessage.

    It contains four fields:

    - `receivers`: a non-empty list of :class:`AIDModel` objects
    - `performative`: the message's performative
    - `conversation_id`: an optional conversation ID to track the conversation
    - `content`: a JSON-serializable message's content

    """

    receivers: List[AIDModel]
    performative: Performative
    conversation_id: Optional[str]
    content: Any
