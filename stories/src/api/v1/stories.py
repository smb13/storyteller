from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models import Story
from schemas.story import StoryResponse
from services.stories import check_permissions
from services.roles import RolesService, get_roles_service

router = APIRouter()


@router.get(
    "/{role_id}",
    response_model=role_schemas.RoleResponse,
    summary="Retrieve a role",
    dependencies=[Depends(check_permissions(ActionEnum.role_read))],
)
async def role_details(
    role_id: UUID,
    roles_service: RolesService = Depends(get_roles_service),
) -> role_schemas.RoleResponse:
    """Retrieve an item with all the information."""

    role: User | None = await roles_service.retrieve(role_id=role_id)
    if not role:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Role not found")

    return role_schemas.RoleResponse.model_validate(role)
