from __future__ import annotations

from typing import Any, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user import UserCreate, UserUpdate


class UserDAO:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._col = db["users"]

    async def create(self, user: UserCreate) -> dict[str, Any]:
        doc = user.model_dump(by_alias=True)
        await self._col.insert_one(doc)
        return doc

    async def get(self, user_id: str) -> Optional[dict[str, Any]]:
        return await self._col.find_one({"_id": user_id})

    async def list(self, *, skip: int = 0, limit: int = 50) -> list[dict[str, Any]]:
        cursor = self._col.find({}, skip=skip, limit=limit)
        return [doc async for doc in cursor]

    async def replace(self, user_id: str, update: UserUpdate) -> Optional[dict[str, Any]]:
        new_doc = update.model_dump(by_alias=True, exclude_unset=True)
        new_doc["_id"] = user_id
        res = await self._col.replace_one({"_id": user_id}, new_doc, upsert=False)
        if res.matched_count == 0:
            return None
        return await self.get(user_id)

    async def patch(self, user_id: str, update: UserUpdate) -> Optional[dict[str, Any]]:
        payload = update.model_dump(by_alias=True, exclude_unset=True)
        if not payload:
            return await self.get(user_id)
        res = await self._col.update_one({"_id": user_id}, {"$set": payload})
        if res.matched_count == 0:
            return None
        return await self.get(user_id)

    async def delete(self, user_id: str) -> bool:
        res = await self._col.delete_one({"_id": user_id})
        return res.deleted_count == 1

