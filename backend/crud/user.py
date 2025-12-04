"""
CRUD操作 - 用户管理
User CRUD operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from models import User, UserRole
from schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int) -> Optional[User]:
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根据邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    role: Optional[UserRole] = None,
    username: Optional[str] = None,
    real_name: Optional[str] = None,
    organization_id: Optional[int] = None
) -> List[User]:
    """获取用户列表"""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    if username:
        query = query.filter(User.username.contains(username))
    if real_name:
        query = query.filter(User.real_name.contains(real_name))
    if organization_id:
        query = query.filter(User.organization_id == organization_id)
    
    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """创建用户"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        real_name=user.real_name,
        email=user.email,
        mobile=user.mobile,
        role=user.role,
        organization_id=user.organization_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """更新用户"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
    """更新用户密码"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db_user.password_hash = get_password_hash(new_password)
    db.commit()
    return True


def delete_user(db: Session, user_id: int) -> bool:
    """删除用户"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """认证用户"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
