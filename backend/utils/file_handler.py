"""
文件处理工具
File handling utilities
"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
from config import settings


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()


def validate_file_type(filename: str) -> bool:
    """验证文件类型"""
    ext = get_file_extension(filename)
    return ext in settings.ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename: str) -> str:
    """生成唯一文件名"""
    ext = get_file_extension(original_filename)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name


async def save_upload_file(
    upload_file: UploadFile,
    subdir: str = "general"
) -> tuple[str, str, int]:
    """
    保存上传文件
    Returns: (filepath, filename, file_size)
    """
    # 验证文件类型
    if not validate_file_type(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。允许的类型: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # 创建上传目录
    upload_dir = Path(settings.UPLOAD_DIR) / subdir
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成唯一文件名
    unique_filename = generate_unique_filename(upload_file.filename)
    file_path = upload_dir / unique_filename
    
    # 保存文件
    content = await upload_file.read()
    file_size = len(content)
    
    # 检查文件大小
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制({settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB)"
        )
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    return str(file_path), unique_filename, file_size


def delete_file(filepath: str) -> bool:
    """删除文件"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception:
        return False
