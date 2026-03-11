from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class OrganizationEntry(BaseModel):
    model_config = ConfigDict(extra="allow")
    person_uuid: str


class AptmRoleEntry(BaseModel):
    model_config = ConfigDict(extra="allow")
    depots: list[str] = Field(default_factory=list)
    analytics: bool = False
    user_class: Optional[str] = None
    aptm_role: Optional[str] = None


class Timeline(BaseModel):
    model_config = ConfigDict(extra="allow")
    created_by: Optional[str] = None
    created_date: Optional[int] = None
    updated_date: Optional[int] = None
    updated_by: Optional[str] = None


class UserBase(BaseModel):
    model_config = ConfigDict(extra="allow")

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    person_id: Optional[str] = None
    uuid: Optional[str] = None

    weight_unit: Optional[str] = None
    volume_unit: Optional[str] = None
    speed_unit: Optional[str] = None
    distance_unit: Optional[str] = None
    date_format: Optional[str] = None
    time: Optional[str] = None

    organization: list[OrganizationEntry] = Field(default_factory=list)
    aptm_role: list[AptmRoleEntry] = Field(default_factory=list)

    is_deleted: bool = False
    is_active: bool = True

    password: Optional[str] = None
    timeline: Optional[Timeline] = None


class UserCreate(UserBase):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "example": {
                "_id": "test_user",
                "first_name": "test",
                "last_name": "user",
                "email": "test_user@project44.com",
                "person_id": "test_user@project44.com",
                "uuid": "8519cfa1-9b8d-453f-bd4f-0661c13abca8",
                "weight_unit": "pounds",
                "date_format": "MM/dd/yyyy",
                "volume_unit": "cubic feet",
                "speed_unit": "miles/hr",
                "time": "hh:mm a",
                "distance_unit": "imperial",
                "organization": [
                    {"ctc": True, "person_uuid": "8519cfa1-9b8d-453f-bd4f-0661c13abca8"},
                    {"yms_test": True, "person_uuid": "8519cfa1-9b8d-453f-bd4f-0661c13abda8"},
                ],
                "aptm_role": [
                    {
                        "depots": ["all"],
                        "analytics": False,
                        "user_class": "org-user",
                        "aptm_role": "admin",
                    }
                ],
                "is_deleted": False,
                "is_active": True,
                "password": "$2b$12$...",
                "timeline": {
                    "created_by": "someone@project44.com",
                    "created_date": 1672395099263,
                    "updated_date": 1691414032442,
                    "updated_by": "someoneelse@project44.com",
                },
            }
        },
    )
    id: str = Field(alias="_id")


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")


class UserOut(UserInDB):
    pass


class DeleteResult(BaseModel):
    deleted: Literal[True] = True
    id: str

