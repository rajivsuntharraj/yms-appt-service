from __future__ import annotations

from app.dao.users import UserDAO
from app.db.mongo import get_database
from app.services.users import UserService


def get_user_service() -> UserService:
    db = get_database()
    return UserService(UserDAO(db))

