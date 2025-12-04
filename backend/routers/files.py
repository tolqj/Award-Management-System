"""
文件管理路由
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils.auth import get_current_user
from utils.file_handler import save_upload_file
from utils.excel_utils import create_application_template, export_applications_to_excel
import os

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    subdir: str = "general",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传文件"""
    filepath, filename, file_size = await save_upload_file(file, subdir)
    
    return {
        "message": "文件上传成功",
        "filename": filename,
        "filepath": filepath,
        "file_size": file_size
    }


@router.get("/download/{file_path:path}")
async def download_file(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """下载文件"""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        file_path,
        filename=os.path.basename(file_path)
    )


@router.get("/template/application")
async def download_application_template():
    """下载申报Excel模板"""
    excel_file = create_application_template()
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=application_template.xlsx"}
    )
