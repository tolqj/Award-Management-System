"""
组织管理路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from crud.organization import get_organizations, get_organization, create_organization, update_organization, delete_organization
from utils.auth import get_current_user, require_role
from models import User, UserRole, OrgType

router = APIRouter()


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    org_type: Optional[str] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取组织列表"""
    # 转换组织类型枚举
    org_type_enum = None
    if org_type:
        try:
            org_type_enum = OrgType(org_type)
        except ValueError:
            pass
    
    return get_organizations(
        db, 
        skip=skip, 
        limit=limit, 
        org_type=org_type_enum,
        name=name
    )


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization_detail(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取组织详情"""
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    return org


@router.post("/", response_model=OrganizationResponse)
async def create_new_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """创建组织"""
    return create_organization(db, org)


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization_info(
    org_id: int,
    org_update: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """更新组织"""
    updated_org = update_organization(db, org_id, org_update)
    if not updated_org:
        raise HTTPException(status_code=404, detail="组织不存在")
    return updated_org


@router.delete("/{org_id}")
async def delete_organization_account(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """删除组织"""
    success = delete_organization(db, org_id)
    if not success:
        raise HTTPException(status_code=404, detail="组织不存在")
    return {"message": "组织删除成功"}
