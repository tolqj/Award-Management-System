"""
评审管理路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from crud.review import (
    get_reviews_by_expert, get_reviews_by_application, get_review,
    create_review, update_review, submit_review,
    assign_expert_to_application, get_application_score_summary
)
from models import User, UserRole
from utils.auth import get_current_user, require_role

router = APIRouter()


@router.get("/my-reviews", response_model=List[ReviewResponse])
async def get_my_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXPERT]))
):
    """获取我的评审任务"""
    reviews = get_reviews_by_expert(db, current_user.id, skip, limit)
    return reviews


@router.get("/application/{app_id}", response_model=List[ReviewResponse])
async def get_application_reviews(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF, UserRole.COMMITTEE]))
):
    """获取某申报的所有评审"""
    reviews = get_reviews_by_application(db, app_id)
    return reviews


@router.post("/", response_model=ReviewResponse)
async def create_or_update_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXPERT]))
):
    """创建或更新评审（草稿）"""
    return create_review(db, review, current_user.id)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review_api(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXPERT]))
):
    """更新评审"""
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="评审不存在")
    
    if db_review.expert_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改他人的评审")
    
    return update_review(db, review_id, review_update)


@router.post("/{review_id}/submit")
async def submit_review_api(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXPERT]))
):
    """提交评审"""
    db_review = get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="评审不存在")
    
    if db_review.expert_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权提交他人的评审")
    
    review = submit_review(db, review_id)
    return {"message": "评审提交成功", "review": review}


@router.post("/assign")
async def assign_expert(
    app_id: int,
    expert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """分配专家评审"""
    review = assign_expert_to_application(db, app_id, expert_id)
    return {"message": "分配成功", "review": review}


@router.get("/score-summary/{app_id}")
async def get_score_summary(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF, UserRole.COMMITTEE]))
):
    """获取申报的评分汇总"""
    summary = get_application_score_summary(db, app_id)
    if not summary:
        return {"message": "暂无评分数据"}
    return summary
