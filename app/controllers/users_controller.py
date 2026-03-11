from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.core.security import get_current_user
from app.dependencies import get_user_service
from app.models.user import DeleteResult, UserCreate, UserOut, UserUpdate
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
) -> UserOut:
    """Create a new user document (Mongo `_id` is required and must be unique)."""
    return await service.create(user)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, service: UserService = Depends(get_user_service)) -> UserOut:
    """Get a user by `_id`."""
    return await service.get(user_id)


@router.get("", response_model=list[UserOut])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    service: UserService = Depends(get_user_service),
) -> list[UserOut]:
    """List users (paginated)."""
    return await service.list(skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserOut)
async def replace_user(
    user_id: str,
    update: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    """Replace an existing user (full update)."""
    return await service.replace(user_id, update)


@router.patch("/{user_id}", response_model=UserOut)
async def patch_user(
    user_id: str,
    update: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    """Patch an existing user (partial update)."""
    return await service.patch(user_id, update)


@router.delete("/{user_id}", response_model=DeleteResult)
async def delete_user(
    user_id: str, service: UserService = Depends(get_user_service)
) -> DeleteResult:
    """Delete a user by `_id`."""
    return await service.delete(user_id)

