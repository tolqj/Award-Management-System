"""测试登录问题"""
from database import SessionLocal
from models import User
from crud.user import verify_password, get_password_hash

db = SessionLocal()

# 查询admin用户
admin = db.query(User).filter(User.username == "admin").first()

if admin:
    print(f"用户名: {admin.username}")
    print(f"密码哈希: {admin.password_hash}")
    print(f"角色: {admin.role}")
    print(f"激活状态: {admin.is_active}")
    
    # 测试密码验证
    test_password = "admin123"
    result = verify_password(test_password, admin.password_hash)
    print(f"\n密码 '{test_password}' 验证结果: {result}")
    
    # 如果验证失败，重新设置密码
    if not result:
        print("\n密码验证失败，重新设置密码...")
        new_hash = get_password_hash(test_password)
        admin.password_hash = new_hash
        db.commit()
        print("密码已重置")
else:
    print("未找到admin用户")

db.close()
