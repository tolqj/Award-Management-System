"""
CRUD操作 - 组织管理
Organization CRUD operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from models import Organization, OrgType
from schemas import OrganizationCreate, OrganizationUpdate


def get_organization(db: Session, org_id: int) -> Optional[Organization]:
    """根据ID获取组织"""
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_organization_by_name(db: Session, name: str) -> Optional[Organization]:
    """根据名称获取组织"""
    return db.query(Organization).filter(Organization.name == name).first()


def get_organization_by_code(db: Session, code: str) -> Optional[Organization]:
    """根据代码获取组织"""
    return db.query(Organization).filter(Organization.code == code).first()


def get_organizations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    org_type: Optional[OrgType] = None,
    name: Optional[str] = None
) -> List[Organization]:
    """获取组织列表"""
    query = db.query(Organization)
    
    if org_type:
        query = query.filter(Organization.org_type == org_type)
    if name:
        query = query.filter(Organization.name.contains(name))
    
    return query.offset(skip).limit(limit).all()


def create_organization(db: Session, org: OrganizationCreate) -> Organization:
    """创建组织"""
    db_org = Organization(**org.model_dump())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def update_organization(
    db: Session, 
    org_id: int, 
    org_update: OrganizationUpdate
) -> Optional[Organization]:
    """更新组织"""
    db_org = get_organization(db, org_id)
    if not db_org:
        return None
    
    update_data = org_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_org, field, value)
    
    db.commit()
    db.refresh(db_org)
    return db_org


def delete_organization(db: Session, org_id: int) -> bool:
    """删除组织"""
    db_org = get_organization(db, org_id)
    if not db_org:
        return False
    
    db.delete(db_org)
    db.commit()
    return True
