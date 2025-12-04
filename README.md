# XXXX协会科学技术奖评审管理系统

## 项目简介

XXXX协会科学技术奖评审管理系统是一个完整的前后端分离Web应用，用于支持科技奖项的申报、评审、公示等全流程管理。

### 技术栈

**后端:**
- Python 3.8+
- FastAPI
- SQLAlchemy
- MySQL 5.7+/8.0+
- JWT认证
- Pydantic数据验证

**前端:**
- Vue 3
- Vite
- Element Plus
- Pinia状态管理
- Vue Router
- Axios
- ECharts图表

## 功能特性

- ✅ 用户认证与权限管理（JWT）
- ✅ 多角色支持（管理员、工作人员、申报人、专家、评委等）
- ✅ 申报在线提交与状态流转
- ✅ 专家匿名评审系统
- ✅ 评审委员会终审决议
- ✅ 公示与异议管理
- ✅ 统计分析与图表展示
- ✅ 文件上传下载
- ✅ Excel导入导出

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+/8.0+

### 1. 克隆项目

```bash
cd 评奖管理系统
```

### 2. 后端安装与配置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置数据库(修改 config.py 中的数据库配置)
# 默认配置:
# DB_HOST: localhost
# DB_PORT: 3306
# DB_USER: root
# DB_PASSWORD: 123456
# DB_NAME: nonferrous_award_system

# 初始化数据库
python setup_database.py
```

### 3. 前端安装

```bash
cd frontend

# 安装依赖
npm install
```

### 4. 启动服务

**Windows:**
```bash
cd deploy
start_all.bat
```

**Linux/macOS:**
```bash
cd deploy
chmod +x start_all.sh
./start_all.sh
```

或手动启动:

```bash
# 终端1 - 启动后端
cd backend
python main.py

# 终端2 - 启动前端
cd frontend
npm run dev
```

### 5. 访问系统

- **前端页面:** http://localhost:5173
- **后端API文档:** http://localhost:8000/docs
- **后端ReDoc:** http://localhost:8000/redoc

### 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 工作人员 | staff01 | staff123 |
| 专家 | expert01 | expert123 |
| 申报人 | applicant01 | app123 |
| 评委 | committee01 | comm123 |

## 项目结构

```
评奖管理系统/
├── backend/                 # 后端代码
│   ├── routers/            # API路由
│   ├── crud/               # 数据库操作
│   ├── utils/              # 工具类
│   ├── models.py           # 数据库模型
│   ├── schemas.py          # Pydantic模型
│   ├── database.py         # 数据库连接
│   ├── config.py           # 配置文件
│   ├── main.py             # 主程序
│   ├── setup_database.py   # 数据库初始化脚本
│   └── requirements.txt    # Python依赖
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 公共组件
│   │   ├── api/            # API封装
│   │   ├── store/          # Pinia状态管理
│   │   ├── router/         # 路由配置
│   │   └── main.js         # 入口文件
│   ├── package.json        # 前端依赖
│   └── vite.config.js      # Vite配置
├── deploy/                  # 部署脚本
│   ├── start_all.bat       # Windows启动脚本
│   ├── start_all.sh        # Linux启动脚本
│   └── nginx.conf          # Nginx配置示例
└── README.md               # 项目说明
```

## 数据库设计

系统包含以下主要数据表:

- **users** - 用户表
- **organizations** - 组织/单位表
- **awards** - 奖项表
- **award_cycles** - 奖项轮次表
- **applications** - 申报表
- **attachments** - 附件表
- **recommenders** - 推荐单位表
- **reviews** - 评审表
- **committee_decisions** - 评审委员会决议表
- **announcements** - 公示表
- **objections** - 异议表
- **logs** - 操作日志表

## API文档

启动后端后访问 http://localhost:8000/docs 查看完整的API文档。

主要API端点:

- `/api/auth/*` - 认证相关
- `/api/users/*` - 用户管理
- `/api/organizations/*` - 组织管理
- `/api/awards/*` - 奖项管理
- `/api/applications/*` - 申报管理
- `/api/reviews/*` - 评审管理
- `/api/committee/*` - 评审委员会
- `/api/announcements/*` - 公示管理
- `/api/statistics/*` - 统计分析
- `/api/files/*` - 文件管理

## 生产部署

### 使用Gunicorn + Nginx

1. 安装Gunicorn:
```bash
pip install gunicorn
```

2. 启动后端:
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. 构建前端:
```bash
cd frontend
npm run build
```

4. 配置Nginx (参考 deploy/nginx.conf)

5. 启动Nginx:
```bash
sudo nginx -c /path/to/nginx.conf
```

### 使用Supervisor管理后端进程

创建配置文件 `/etc/supervisor/conf.d/nonferrous_award.conf`:

```ini
[program:nonferrous_award]
directory=/var/www/nonferrous-award/backend
command=gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
autostart=true
autorestart=true
stderr_logfile=/var/log/nonferrous_award.err.log
stdout_logfile=/var/log/nonferrous_award.out.log
```

## 安全建议

生产环境部署时请注意:

1. 修改 `config.py` 中的 `SECRET_KEY`
2. 修改默认数据库密码
3. 启用HTTPS
4. 配置防火墙
5. 定期备份数据库
6. 修改所有默认用户密码
7. 限制文件上传大小和类型

## 常见问题

### 1. 数据库连接失败

检查 MySQL 服务是否启动，配置文件中的数据库信息是否正确。

### 2. 前端无法连接后端

检查后端是否启动，CORS配置是否正确。

### 3. 文件上传失败

检查 `backend/uploads/` 目录是否存在且有写权限。

## 许可证

本项目仅供学习和演示使用。

## 联系方式

如有问题请提Issue或联系开发团队。

---

**XXXX协会科学技术奖评审管理系统** v1.0.0
