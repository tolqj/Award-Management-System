"""
用户管理路由
User management routes
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserUpdate, UserResponse, PaginatedResponse
from crud.user import get_users, get_user, create_user, update_user, delete_user, get_user_by_username, get_user_by_email
from utils.auth import get_current_user, require_role
from models import User, UserRole

router = APIRouter()


@router.get("/", response_model=List[UserResponse], summary="获取用户列表")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    username: Optional[str] = None,
    real_name: Optional[str] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """
    获取用户列表
    需要管理员或工作人员权限
    """
    # 转换角色枚举
    role_enum = None
    if role:
        try:
            role_enum = UserRole(role)
        except ValueError:
            pass
    
    users = get_users(
        db, 
        skip=skip, 
        limit=limit, 
        role=role_enum, 
        username=username,
        real_name=real_name,
        organization_id=organization_id
    )
    return users


@router.get("/{user_id}", response_model=UserResponse, summary="获取用户详情")
async def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户详情
    需要认证
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/", response_model=UserResponse, summary="创建用户")
async def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """
    创建新用户
    需要管理员或工作人员权限
    """
    # 检查用户名是否存在
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否存在
    if user.email and get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已被使用")
    
    return create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user_info(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.STAFF]))
):
    """
    更新用户信息
    需要管理员或工作人员权限
    """
    updated_user = update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user


@router.delete("/{user_id}", summary="删除用户")
async def delete_user_account(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """
    删除用户
    需要管理员权限
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}
