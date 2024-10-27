from typing import List
from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str
    description: str
    owner_id: str
    members: List[str]
