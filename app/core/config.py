from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    mongodb_uri: str
    mongodb_db: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_audience: str
    jwt_issuer: str


def _env(name: str, default: str) -> str:
    val = os.getenv(name)
    return val if val is not None and val != "" else default


settings = Settings(
    mongodb_uri=_env("MONGODB_URI", "mongodb://localhost:27017"),
    mongodb_db=_env("MONGODB_DB", "yms_appt_service"),
    jwt_secret=_env("JWT_SECRET", "dev-secret-change-me"),
    jwt_algorithm=_env("JWT_ALGORITHM", "HS256"),
    jwt_audience=_env("JWT_AUDIENCE", ""),
    jwt_issuer=_env("JWT_ISSUER", ""),
)

