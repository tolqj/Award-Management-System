"""
CRUD操作 - 评审管理
Review CRUD operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import Review, Application, ApplicationStatus
from schemas import ReviewCreate, ReviewUpdate


def get_review(db: Session, review_id: int) -> Optional[Review]:
    """根据ID获取评审"""
    return db.query(Review).filter(Review.id == review_id).first()


def get_review_by_expert_and_app(
    db: Session,
    expert_id: int,
    app_id: int
) -> Optional[Review]:
    """获取专家对某申报的评审"""
    return db.query(Review).filter(
        Review.expert_id == expert_id,
        Review.application_id == app_id
    ).first()


def get_reviews_by_expert(
    db: Session,
    expert_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Review]:
    """获取专家的所有评审"""
    return db.query(Review).filter(
        Review.expert_id == expert_id
    ).offset(skip).limit(limit).all()


def get_reviews_by_application(
    db: Session,
    app_id: int
) -> List[Review]:
    """获取某申报的所有评审"""
    return db.query(Review).filter(
        Review.application_id == app_id
    ).all()


def create_review(
    db: Session,
    review: ReviewCreate,
    expert_id: int
) -> Review:
    """创建评审"""
    db_review = Review(
        application_id=review.application_id,
        expert_id=expert_id,
        scores_json=review.scores_json,
        total_score=review.total_score,
        comment=review.comment,
        status="draft"
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(
    db: Session,
    review_id: int,
    review_update: ReviewUpdate
) -> Optional[Review]:
    """更新评审"""
    db_review = get_review(db, review_id)
    if not db_review:
        return None
    
    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review


def submit_review(db: Session, review_id: int) -> Optional[Review]:
    """提交评审"""
    db_review = get_review(db, review_id)
    if not db_review:
        return None
    
    db_review.status = "submitted"
    db_review.submitted_at = datetime.now()
    
    db.commit()
    db.refresh(db_review)
    
    # 更新申报的评分汇总
    update_application_scores(db, db_review.application_id)
    
    return db_review


def update_application_scores(db: Session, app_id: int) -> None:
    """更新申报的评分汇总"""
    reviews = get_reviews_by_application(db, app_id)
    
    if not reviews:
        return
    
    # 只统计已提交的评审
    submitted_reviews = [r for r in reviews if r.status == "submitted"]
    
    if not submitted_reviews:
        return
    
    # 计算平均分
    total_scores = [r.total_score for r in submitted_reviews if r.total_score]
    
    if total_scores:
        avg_score = sum(total_scores) / len(total_scores)
        
        score_summary = {
            "average_score": round(avg_score, 2),
            "review_count": len(submitted_reviews),
            "scores": total_scores,
            "max_score": max(total_scores),
            "min_score": min(total_scores)
        }
        
        # 更新申报的评分汇总
        application = db.query(Application).filter(Application.id == app_id).first()
        if application:
            application.score_summary_json = score_summary
            db.commit()


def assign_expert_to_application(
    db: Session,
    app_id: int,
    expert_id: int
) -> Review:
    """分配专家评审申报"""
    # 检查是否已分配
    existing = get_review_by_expert_and_app(db, expert_id, app_id)
    if existing:
        return existing
    
    # 创建评审记录
    db_review = Review(
        application_id=app_id,
        expert_id=expert_id,
        status="pending"
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_application_score_summary(db: Session, app_id: int) -> Optional[Dict[str, Any]]:
    """获取申报的评分汇总"""
    reviews = get_reviews_by_application(db, app_id)
    submitted_reviews = [r for r in reviews if r.status == "submitted"]
    
    if not submitted_reviews:
        return None
    
    total_scores = [r.total_score for r in submitted_reviews if r.total_score]
    
    if not total_scores:
        return None
    
    return {
        "average_score": round(sum(total_scores) / len(total_scores), 2),
        "review_count": len(submitted_reviews),
        "total_assigned": len(reviews),
        "scores": total_scores,
        "max_score": max(total_scores),
        "min_score": min(total_scores),
        "median_score": sorted(total_scores)[len(total_scores) // 2]
    }
