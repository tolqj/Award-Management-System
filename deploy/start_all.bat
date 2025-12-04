@echo off
chcp 65001 >nul
echo ========================================
echo XXXX协会科学技术奖评审管理系统
echo 启动脚本 (Windows)
echo ========================================
echo.

echo [1/3] 启动后端服务...
cd backend
start "后端服务" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [2/3] 启动前端服务...
cd ..\frontend
start "前端服务" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 服务启动完成!
echo ========================================
echo 后端API: http://localhost:8000
echo 后端文档: http://localhost:8000/docs
echo 前端页面: http://localhost:5173
echo ========================================
echo.
echo 按任意键关闭此窗口...
pause >nul
