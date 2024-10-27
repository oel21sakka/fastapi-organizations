from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any


class OrganizationBase(BaseModel):
    name: str
    description: str


class OrganizationInDB(OrganizationBase):
    id: str = Field(alias="_id")
    owner_id: str
    members: List[str]


class OrganizationResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    owner_id: str


class UserInOrganization(BaseModel):
    name: str
    email: str


class OrganizationWithMembersResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    owner_id: str
    members: List[Any]


class OrganizationUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class AddMemberRequest(BaseModel):
    email: EmailStr
