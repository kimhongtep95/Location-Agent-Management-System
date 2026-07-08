from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.application.services.agent_service import AgentService
from app.core.dependencies import CurrentUser, get_agent_service, get_current_user
from app.presentation.api.v1.schemas import (
    AgentResponse,
    CreateAgentRequest,
    UpdateAgentRequest,
    agent_to_response,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=list[AgentResponse])
async def list_agents(
    status: str | None = Query(default=None),
    region: str | None = Query(default=None),
    _: CurrentUser = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
) -> list[AgentResponse]:
    agents = await service.list_agents(status=status, region=region)
    return [agent_to_response(agent) for agent in agents]


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: CreateAgentRequest,
    _: CurrentUser = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    agent = await service.create_agent(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        region=payload.region,
        status=payload.status.value,
    )
    return agent_to_response(agent)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    agent = await service.get_agent(agent_id)
    return agent_to_response(agent)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    payload: UpdateAgentRequest,
    _: CurrentUser = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    agent = await service.update_agent(
        agent_id,
        **payload.model_dump(exclude_unset=True),
    )
    return agent_to_response(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    _: CurrentUser = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
) -> None:
    await service.delete_agent(agent_id)
