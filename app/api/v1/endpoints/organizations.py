from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.core.security import get_current_user
from app.schemas.organization import OrganizationBase, OrganizationUpdate, OrganizationResponse, OrganizationWithMembersResponse, AddMemberRequest
from app.schemas.user import UserInDB, User
from app.services.organization_service import (
    create_organization, get_organizations, get_organization, update_organization, delete_organization,
    add_member_to_organization, remove_member_from_organization
)

router = APIRouter()

@router.post("/", response_model=OrganizationResponse)
async def create_org(org: OrganizationBase, current_user: UserInDB = Depends(get_current_user)):
    return await create_organization(org, current_user.id)

@router.get("/", response_model=List[OrganizationResponse])
async def list_orgs(current_user: UserInDB = Depends(get_current_user)):
    return await get_organizations()

@router.get("/{org_id}", response_model=OrganizationWithMembersResponse)
async def get_org(org_id: str, current_user: UserInDB = Depends(get_current_user)):
    org = await get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_org(
    org_id: str,
    org_update: OrganizationUpdate,
    current_user: User = Depends(get_current_user)
):
    org = await get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    if org.owner_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this organization")
    
    return await update_organization(org_id, org_update)

@router.delete("/{org_id}", status_code=204)
async def delete_org(org_id: str, current_user: UserInDB = Depends(get_current_user)):
    org = await get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.owner_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this organization")
    success = await delete_organization(org_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")

@router.post("/{org_id}/invite", status_code=204)
async def add_member(
    org_id: str,
    request: AddMemberRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    org = await get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.owner_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to add members to this organization")
    
    success = await add_member_to_organization(org_id, request.email)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add member to organization")
