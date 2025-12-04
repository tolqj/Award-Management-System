"""
评审委员会路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import CommitteeDecisionCreate, CommitteeDecisionResponse
from models import User, UserRole, CommitteeDecision
from utils.auth import get_current_user, require_role

router = APIRouter()


@router.get("/decisions", response_model=List[CommitteeDecisionResponse])
async def list_decisions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF, UserRole.COMMITTEE]))
):
    """获取所有决议"""
    decisions = db.query(CommitteeDecision).offset(skip).limit(limit).all()
    return decisions


@router.get("/decisions/{decision_id}", response_model=CommitteeDecisionResponse)
async def get_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF, UserRole.COMMITTEE]))
):
    """获取决议详情"""
    decision = db.query(CommitteeDecision).filter(CommitteeDecision.id == decision_id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.post("/decisions", response_model=CommitteeDecisionResponse)
async def create_decision(
    decision: CommitteeDecisionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.COMMITTEE, UserRole.ADMIN]))
):
    """创建评审委员会决议"""
    db_decision = CommitteeDecision(
        **decision.model_dump(),
        decided_by=current_user.id
    )
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision


@router.put("/decisions/{decision_id}", response_model=CommitteeDecisionResponse)
async def update_decision(
    decision_id: int,
    decision: CommitteeDecisionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """更新决议"""
    db_decision = db.query(CommitteeDecision).filter(CommitteeDecision.id == decision_id).first()
    if not db_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    for key, value in decision.model_dump().items():
        setattr(db_decision, key, value)
    
    db.commit()
    db.refresh(db_decision)
    return db_decision


@router.delete("/decisions/{decision_id}")
async def delete_decision(
    decision_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """删除决议"""
    db_decision = db.query(CommitteeDecision).filter(CommitteeDecision.id == decision_id).first()
    if not db_decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    db.delete(db_decision)
    db.commit()
    return {"message": "Decision deleted successfully"}


@router.get("/decisions/application/{app_id}", response_model=List[CommitteeDecisionResponse])
async def get_application_decisions(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取某申报的决议"""
    decisions = db.query(CommitteeDecision).filter(
        CommitteeDecision.application_id == app_id
    ).all()
    return decisions
