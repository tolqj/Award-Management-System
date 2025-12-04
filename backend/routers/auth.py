"""
认证路由
Authentication routes
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import Token, LoginRequest, UserResponse, PasswordChange
from crud.user import authenticate_user, get_user, update_user_password
from utils.auth import create_access_token, get_current_user
from config import settings
from models import User

router = APIRouter()


@router.post("/login", response_model=Token, summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录
    - **username**: 用户名
    - **password**: 密码
    
    返回JWT访问令牌
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    需要认证
    """
    return current_user


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改当前用户密码
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    # 验证旧密码
    user = authenticate_user(db, current_user.username, password_data.old_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 更新密码
    success = update_user_password(db, current_user.id, password_data.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码更新失败"
        )
    
    return {"message": "密码修改成功"}


@router.post("/logout", summary="用户登出")
async def logout(current_user: User = Depends(get_current_user)):
    """
    用户登出（前端清除token即可）
    """
    return {"message": "登出成功"}
