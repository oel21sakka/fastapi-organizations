from pydantic import EmailStr
from app.schemas.organization import OrganizationBase, OrganizationResponse, OrganizationUpdate, OrganizationInDB, OrganizationWithMembersResponse, UserInOrganization
from app.database.mongodb import organizations_collection, users_collection
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from app.services.auth_service import get_user_by_email

async def create_organization(org: OrganizationBase, owner_id: str):
    org_dict = org.dict()
    org_dict["owner_id"] = owner_id
    org_dict["members"] = [owner_id]
    org_dict["created_at"] = datetime.utcnow()
    org_dict["updated_at"] = datetime.utcnow()
    result = await organizations_collection.insert_one(org_dict)
    created_org = await organizations_collection.find_one({"_id": ObjectId(oid=result.inserted_id)})
    created_org['_id'] = str(created_org['_id'])
    return OrganizationResponse(**created_org)

async def get_organizations():
    cursor = organizations_collection.find()
    organizations = await cursor.to_list(length=None)
    for org in organizations:
        org['_id'] = str(org['_id'])
    return [OrganizationResponse(**org) for org in organizations]

async def get_organization(org_id: str) -> OrganizationWithMembersResponse | None:
    org = await organizations_collection.find_one({"_id": ObjectId(org_id)})
    if org:
        org['_id'] = str(org['_id'])        
        members_cursor = users_collection.find(
            {"_id": {"$in": [ObjectId(member_id) for member_id in org["members"]]}},
        )
        members = [UserInOrganization(**member) for member in await members_cursor.to_list(length=None)]        
        org.pop("members", None)
        
        return OrganizationWithMembersResponse(**org, members=members)
    return None

async def update_organization(org_id: str, org_update: OrganizationUpdate):
    update_data = org_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    if update_data:
        result = await organizations_collection.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": update_data}
        )
        if result.modified_count == 1:
            updated_org = await organizations_collection.find_one({"_id": ObjectId(org_id)})
            updated_org['_id'] = str(updated_org['_id'])
            print(updated_org)
            return OrganizationResponse(**updated_org)
    
    return None

async def delete_organization(org_id: str):
    result = await organizations_collection.delete_one({"_id": ObjectId(org_id)})
    return result.deleted_count > 0

async def add_member_to_organization(org_id: str, email: EmailStr):
    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # Raise a 404 error if the user is not found
    
    result = await organizations_collection.update_one(
        {"_id": ObjectId(org_id)},
        {"$addToSet": {"members": ObjectId(user.id)}}
    )
    return result.modified_count > 0

async def remove_member_from_organization(org_id: str, user_id: str):
    result = await organizations_collection.update_one(
        {"_id": ObjectId(org_id)},
        {"$pull": {"members": ObjectId(user_id)}}
    )
    return result.modified_count > 0
