"""
申报管理路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationStatusUpdate
from crud.application import (
    get_applications, get_application, create_application, update_application,
    submit_application, update_application_status, delete_application,
    add_attachment, get_attachments
)
from models import User, UserRole, ApplicationStatus
from utils.auth import get_current_user, require_role
from utils.file_handler import save_upload_file

router = APIRouter()


@router.get("/", response_model=List[ApplicationResponse])
async def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    award_cycle_id: Optional[int] = None,
    status: Optional[str] = None,
    title: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取申报列表"""
    # 根据角色过滤
    applicant_unit_id = None
    if current_user.role == UserRole.APPLICANT:
        applicant_unit_id = current_user.organization_id
    
    # 转换状态
    status_enum = None
    if status:
        try:
            status_enum = ApplicationStatus(status)
        except ValueError:
            pass
    
    applications = get_applications(
        db,
        skip=skip,
        limit=limit,
        award_cycle_id=award_cycle_id,
        applicant_unit_id=applicant_unit_id,
        status=status_enum,
        title=title
    )
    return applications


@router.get("/{app_id}", response_model=ApplicationResponse)
async def get_application_detail(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取申报详情"""
    application = get_application(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="申报不存在")
    
    # 权限检查
    if current_user.role == UserRole.APPLICANT:
        if application.applicant_unit_id != current_user.organization_id:
            raise HTTPException(status_code=403, detail="无权访问")
    
    return application


@router.post("/", response_model=ApplicationResponse)
async def create_new_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.APPLICANT, UserRole.RECOMMENDER]))
):
    """创建申报"""
    return create_application(db, application, current_user.id)


@router.put("/{app_id}", response_model=ApplicationResponse)
async def update_application_info(
    app_id: int,
    app_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新申报"""
    application = get_application(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="申报不存在")
    
    # 只能修改草稿状态的申报
    if application.submission_status != ApplicationStatus.DRAFT:
        raise HTTPException(status_code=400, detail="只能修改草稿状态的申报")
    
    updated_app = update_application(db, app_id, app_update)
    return updated_app


@router.post("/{app_id}/submit")
async def submit_application_api(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交申报"""
    application = submit_application(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="申报不存在")
    return {"message": "提交成功", "application": application}


@router.put("/{app_id}/status")
async def update_application_status_api(
    app_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF, UserRole.COMMITTEE]))
):
    """更新申报状态"""
    application = update_application_status(
        db,
        app_id,
        status_update.status,
        status_update.note
    )
    if not application:
        raise HTTPException(status_code=404, detail="申报不存在")
    return {"message": "状态更新成功", "application": application}


@router.post("/{app_id}/attachments")
async def upload_attachment(
    app_id: int,
    file: UploadFile = File(...),
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传附件"""
    # 检查申报是否存在
    application = get_application(db, app_id)
    if not application:
        raise HTTPException(status_code=404, detail="申报不存在")
    
    # 保存文件
    filepath, filename, file_size = await save_upload_file(file, subdir=f"applications/{app_id}")
    
    # 获取文件类型
    file_ext = filename.split('.')[-1] if '.' in filename else ''
    
    # 添加附件记录
    attachment = add_attachment(
        db,
        app_id=app_id,
        filename=file.filename,
        filepath=filepath,
        file_type=file_ext,
        file_size=file_size,
        user_id=current_user.id,
        description=description
    )
    
    return {"message": "上传成功", "attachment": attachment}


@router.get("/{app_id}/attachments")
async def list_attachments(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取申报附件列表"""
    attachments = get_attachments(db, app_id)
    return attachments


@router.delete("/{app_id}")
async def delete_application_api(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.APPLICANT]))
):
    """删除申报"""
    success = delete_application(db, app_id)
    if not success:
        raise HTTPException(status_code=400, detail="只能删除草稿状态的申报")
    return {"message": "删除成功"}
