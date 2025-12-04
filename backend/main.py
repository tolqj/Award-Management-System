"""
XXXX协会科学技术奖评审管理系统 - 主程序
XXXX Association Technology Award Management System - Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from database import engine, Base
import os

# 创建数据库表
# Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="XXXX协会科学技术奖评审管理系统API文档",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# 静态文件服务
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# 导入路由
from routers import auth, users, organizations, awards, applications, reviews, committee, announcements, files, statistics

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["组织管理"])
app.include_router(awards.router, prefix="/api/awards", tags=["奖项管理"])
app.include_router(applications.router, prefix="/api/applications", tags=["申报管理"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["评审管理"])
app.include_router(committee.router, prefix="/api/committee", tags=["评审委员会"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["公示管理"])
app.include_router(files.router, prefix="/api/files", tags=["文件管理"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计分析"])


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": "欢迎使用XXXX协会科学技术奖评审管理系统",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
