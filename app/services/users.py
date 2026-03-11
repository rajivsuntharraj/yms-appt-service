from __future__ import annotations

from fastapi import HTTPException, status

from app.dao.users import UserDAO
from app.models.user import DeleteResult, UserCreate, UserOut, UserUpdate


class UserService:
    def __init__(self, dao: UserDAO):
        self._dao = dao

    async def create(self, user: UserCreate) -> UserOut:
        existing = await self._dao.get(user.id)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{user.id}' already exists",
            )
        doc = await self._dao.create(user)
        return UserOut.model_validate(doc)

    async def get(self, user_id: str) -> UserOut:
        doc = await self._dao.get(user_id)
        if doc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut.model_validate(doc)

    async def list(self, *, skip: int = 0, limit: int = 50) -> list[UserOut]:
        docs = await self._dao.list(skip=skip, limit=limit)
        return [UserOut.model_validate(d) for d in docs]

    async def replace(self, user_id: str, update: UserUpdate) -> UserOut:
        doc = await self._dao.replace(user_id, update)
        if doc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut.model_validate(doc)

    async def patch(self, user_id: str, update: UserUpdate) -> UserOut:
        doc = await self._dao.patch(user_id, update)
        if doc is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut.model_validate(doc)

    async def delete(self, user_id: str) -> DeleteResult:
        ok = await self._dao.delete(user_id)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return DeleteResult(id=user_id)

