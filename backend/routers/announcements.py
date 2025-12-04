"""
公示管理路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from schemas import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse, ObjectionCreate, ObjectionResponse
from models import User, UserRole, Announcement, Objection
from utils.auth import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[AnnouncementResponse])
async def list_announcements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取公示列表（公开）"""
    announcements = db.query(Announcement).filter(
        Announcement.status == "active"
    ).offset(skip).limit(limit).all()
    return announcements


@router.get("/{announcement_id}", response_model=AnnouncementResponse)
async def get_announcement(
    announcement_id: int,
    db: Session = Depends(get_db)
):
    """获取公示详情（公开）"""
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="公示不存在")
    return announcement


@router.post("/", response_model=AnnouncementResponse)
async def create_announcement(
    announcement: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """创建公示"""
    db_announcement = Announcement(
        **announcement.model_dump(),
        created_by=current_user.id
    )
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_announcement(
    announcement_id: int,
    announcement_update: AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """更新公示"""
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="公示不存在")
    
    update_data = announcement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_announcement, field, value)
    
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


# ================ 异议管理 ================
@router.post("/{announcement_id}/objections", response_model=ObjectionResponse)
async def create_objection(
    announcement_id: int,
    objection: ObjectionCreate,
    db: Session = Depends(get_db)
):
    """提交异议（公开接口）"""
    db_objection = Objection(**objection.model_dump())
    db.add(db_objection)
    db.commit()
    db.refresh(db_objection)
    return db_objection


@router.get("/{announcement_id}/objections", response_model=List[ObjectionResponse])
async def list_objections(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """获取公示的异议列表"""
    objections = db.query(Objection).filter(
        Objection.announcement_id == announcement_id
    ).all()
    return objections
