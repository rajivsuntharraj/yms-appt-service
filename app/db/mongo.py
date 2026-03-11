from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: Optional[AsyncIOMotorClient] = None


def connect_to_mongo() -> None:
    global _client
    if _client is None:
        # AsyncIOMotorClient is thread-safe and intended to be shared.
        _client = AsyncIOMotorClient(settings.mongodb_uri)


def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_database() -> AsyncIOMotorDatabase:
    if _client is None:
        connect_to_mongo()
    assert _client is not None
    return _client[settings.mongodb_db]

