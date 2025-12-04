"""
CRUD操作 - 申报管理
Application CRUD operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from models import Application, ApplicationStatus, Attachment
from schemas import ApplicationCreate, ApplicationUpdate


def get_application(db: Session, app_id: int) -> Optional[Application]:
    """根据ID获取申报"""
    return db.query(Application).filter(Application.id == app_id).first()


def get_applications(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    award_cycle_id: Optional[int] = None,
    applicant_unit_id: Optional[int] = None,
    status: Optional[ApplicationStatus] = None,
    title: Optional[str] = None
) -> List[Application]:
    """获取申报列表"""
    query = db.query(Application)
    
    if award_cycle_id:
        query = query.filter(Application.award_cycle_id == award_cycle_id)
    if applicant_unit_id:
        query = query.filter(Application.applicant_unit_id == applicant_unit_id)
    if status:
        query = query.filter(Application.submission_status == status)
    if title:
        query = query.filter(Application.title.like(f'%{title}%'))
    
    return query.order_by(Application.created_at.desc()).offset(skip).limit(limit).all()


def create_application(
    db: Session, 
    app: ApplicationCreate,
    user_id: int
) -> Application:
    """创建申报"""
    db_app = Application(
        **app.model_dump(),
        applicant_user_id=user_id,
        submission_status=ApplicationStatus.DRAFT
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def update_application(
    db: Session,
    app_id: int,
    app_update: ApplicationUpdate
) -> Optional[Application]:
    """更新申报"""
    db_app = get_application(db, app_id)
    if not db_app:
        return None
    
    update_data = app_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_app, field, value)
    
    db.commit()
    db.refresh(db_app)
    return db_app


def submit_application(db: Session, app_id: int) -> Optional[Application]:
    """提交申报"""
    db_app = get_application(db, app_id)
    if not db_app:
        return None
    
    db_app.submission_status = ApplicationStatus.SUBMITTED
    db_app.submission_time = datetime.now()
    db_app.current_stage = "已提交待推荐"
    
    db.commit()
    db.refresh(db_app)
    return db_app


def update_application_status(
    db: Session,
    app_id: int,
    status: ApplicationStatus,
    note: Optional[str] = None
) -> Optional[Application]:
    """更新申报状态"""
    db_app = get_application(db, app_id)
    if not db_app:
        return None
    
    db_app.submission_status = status
    
    # 根据状态更新阶段说明
    stage_mapping = {
        ApplicationStatus.RECOMMENDED: "推荐通过待初审",
        ApplicationStatus.PRELIMINARY_APPROVED: "初审通过待专家评审",
        ApplicationStatus.PRELIMINARY_REJECTED: "初审不通过",
        ApplicationStatus.EXPERT_REVIEW: "专家评审中",
        ApplicationStatus.COMMITTEE_REVIEW: "评委会终审中",
        ApplicationStatus.APPROVED: "终审通过",
        ApplicationStatus.REJECTED: "终审不通过",
        ApplicationStatus.ANNOUNCED: "公示中",
        ApplicationStatus.ARCHIVED: "已归档"
    }
    
    if status in stage_mapping:
        db_app.current_stage = stage_mapping[status]
    
    db.commit()
    db.refresh(db_app)
    return db_app


def delete_application(db: Session, app_id: int) -> bool:
    """删除申报"""
    db_app = get_application(db, app_id)
    if not db_app:
        return False
    
    # 只能删除草稿状态的申报
    if db_app.submission_status != ApplicationStatus.DRAFT:
        return False
    
    db.delete(db_app)
    db.commit()
    return True


def add_attachment(
    db: Session,
    app_id: int,
    filename: str,
    filepath: str,
    file_type: str,
    file_size: int,
    user_id: int,
    description: Optional[str] = None
) -> Attachment:
    """添加附件"""
    db_attachment = Attachment(
        application_id=app_id,
        filename=filename,
        filepath=filepath,
        file_type=file_type,
        file_size=file_size,
        uploaded_by=user_id,
        description=description
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def get_attachments(db: Session, app_id: int) -> List[Attachment]:
    """获取申报的所有附件"""
    return db.query(Attachment).filter(Attachment.application_id == app_id).all()
