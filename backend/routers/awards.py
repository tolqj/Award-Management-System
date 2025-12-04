"""
奖项管理路由 - Awards & AwardCycles
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import AwardCreate, AwardUpdate, AwardResponse, AwardCycleCreate, AwardCycleUpdate, AwardCycleResponse
from models import User, UserRole, Award, AwardCycle
from utils.auth import get_current_user, require_role

router = APIRouter()


# ================ 奖项管理 ================
@router.get("/", response_model=List[AwardResponse])
async def list_awards(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取奖项列表"""
    awards = db.query(Award).offset(skip).limit(limit).all()
    return awards


@router.get("/{award_id}", response_model=AwardResponse)
async def get_award(
    award_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取奖项详情"""
    award = db.query(Award).filter(Award.id == award_id).first()
    if not award:
        raise HTTPException(status_code=404, detail="奖项不存在")
    return award


@router.post("/", response_model=AwardResponse)
async def create_award(
    award: AwardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """创建奖项"""
    db_award = Award(**award.model_dump(), created_by=current_user.id)
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award


@router.put("/{award_id}", response_model=AwardResponse)
async def update_award(
    award_id: int,
    award_update: AwardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """更新奖项"""
    db_award = db.query(Award).filter(Award.id == award_id).first()
    if not db_award:
        raise HTTPException(status_code=404, detail="奖项不存在")
    
    update_data = award_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_award, field, value)
    
    db.commit()
    db.refresh(db_award)
    return db_award


# ================ 奖项轮次管理 ================
@router.get("/cycles/", response_model=List[AwardCycleResponse])
async def list_award_cycles(
    award_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取奖项轮次列表"""
    query = db.query(AwardCycle)
    if award_id:
        query = query.filter(AwardCycle.award_id == award_id)
    cycles = query.offset(skip).limit(limit).all()
    return cycles


@router.post("/cycles/", response_model=AwardCycleResponse)
async def create_award_cycle(
    cycle: AwardCycleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """创建奖项轮次"""
    db_cycle = AwardCycle(**cycle.model_dump())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle


@router.get("/cycles/{cycle_id}", response_model=AwardCycleResponse)
async def get_award_cycle(
    cycle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取奖项轮次详情"""
    cycle = db.query(AwardCycle).filter(AwardCycle.id == cycle_id).first()
    if not cycle:
        raise HTTPException(status_code=404, detail="轮次不存在")
    return cycle
