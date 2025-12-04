"""
统计分析路由
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import User, UserRole, Application, Organization, Review, ApplicationStatus
from utils.auth import get_current_user, require_role
from utils.excel_utils import export_applications_to_excel, export_statistics_to_excel

router = APIRouter()


@router.get("/overview")
async def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """获取统计概览"""
    total_applications = db.query(Application).count()
    total_organizations = db.query(Organization).count()
    total_experts = db.query(User).filter(User.role == UserRole.EXPERT).count()
    total_reviews = db.query(Review).count()
    
    # 按状态统计申报
    status_stats = db.query(
        Application.submission_status,
        func.count(Application.id)
    ).group_by(Application.submission_status).all()
    
    application_by_status = {str(status): count for status, count in status_stats}
    
    # 按组织类型统计申报
    org_type_stats = db.query(
        Organization.org_type,
        func.count(Application.id)
    ).join(Application, Organization.id == Application.applicant_unit_id)\
     .group_by(Organization.org_type).all()
    
    application_by_org_type = {str(org_type): count for org_type, count in org_type_stats}
    
    return {
        "total_applications": total_applications,
        "total_organizations": total_organizations,
        "total_experts": total_experts,
        "total_reviews": total_reviews,
        "application_by_status": application_by_status,
        "application_by_org_type": application_by_org_type
    }


@router.get("/applications-by-status")
async def get_applications_by_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按状态统计申报数"""
    status_stats = db.query(
        Application.submission_status,
        func.count(Application.id)
    ).group_by(Application.submission_status).all()
    
    return [
        {"status": str(status), "count": count}
        for status, count in status_stats
    ]


@router.get("/applications-by-year")
async def get_applications_by_year(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """按年度统计申报数"""
    year_stats = db.query(
        func.year(Application.created_at).label('year'),
        func.count(Application.id).label('count')
    ).group_by('year').all()
    
    return [
        {"year": year, "count": count}
        for year, count in year_stats
    ]


@router.get("/export/applications")
async def export_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """导出申报列表Excel"""
    applications = db.query(Application).all()
    
    # 转换为字典列表
    app_data = []
    for app in applications:
        app_data.append({
            "title": app.title,
            "unit_name": app.applicant_unit.name if app.applicant_unit else "",
            "leader_name": app.leader_name,
            "status": str(app.submission_status),
            "submission_time": app.submission_time,
            "current_stage": app.current_stage,
            "score_summary_json": app.score_summary_json,
            "final_result": app.final_result
        })
    
    excel_file = export_applications_to_excel(app_data)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=applications_export.xlsx"}
    )


@router.get("/export/statistics")
async def export_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """导出统计数据Excel"""
    # 获取统计数据
    overview_data = await get_overview(db, current_user)
    status_data = await get_applications_by_status(db, current_user)
    
    statistics = {
        "overview": overview_data,
        "application_by_status": {item["status"]: item["count"] for item in status_data}
    }
    
    excel_file = export_statistics_to_excel(statistics)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=statistics_export.xlsx"}
    )
