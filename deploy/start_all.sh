#!/bin/bash
echo "========================================"
echo "XXXX协会科学技术奖评审管理系统"
echo "启动脚本 (Linux/macOS)"
echo "========================================"
echo ""

echo "[1/3] 启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!
sleep 2

echo "[2/3] 启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
sleep 2

echo ""
echo "========================================"
echo "服务启动完成!"
echo "========================================"
echo "后端API: http://localhost:8000"
echo "后端文档: http://localhost:8000/docs"
echo "前端页面: http://localhost:5173"
echo "========================================"
echo "后端PID: $BACKEND_PID"
echo "前端PID: $FRONTEND_PID"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"

# 等待
wait
