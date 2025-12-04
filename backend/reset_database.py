"""重置数据库"""
import pymysql
from config import settings

# 连接MySQL服务器
connection = pymysql.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD
)

try:
    with connection.cursor() as cursor:
        # 删除数据库
        cursor.execute(f"DROP DATABASE IF EXISTS `{settings.DB_NAME}`")
        print(f"✓ 数据库 '{settings.DB_NAME}' 已删除")
        
        # 重新创建数据库
        cursor.execute(
            f"CREATE DATABASE `{settings.DB_NAME}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"✓ 数据库 '{settings.DB_NAME}' 已重新创建")
    
    connection.commit()
    print("\n现在请运行: python setup_database.py")
    
finally:
    connection.close()
