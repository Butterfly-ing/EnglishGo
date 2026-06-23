# EnglishGo - 英文学习平台

基于 **Django + Vue3** 的全栈英文学习网站。

## 项目结构

```
web1/
├── 设计/                      # 设计文档
│   ├── 设计说明.md
│   └── API文档.md
├── backend/                   # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/               # Django 配置
│   ├── users/                # 用户模块
│   ├── vocabulary/           # 词汇模块
│   ├── quiz/                 # 测验模块
│   ├── progress/             # 进度模块
│   └── db/                   # SQLite 数据库文件
├── frontend/                  # Vue3 前端
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── api/              # API 请求层
│       ├── router/           # 路由配置
│       ├── stores/           # Pinia 状态管理
│       ├── views/            # 页面组件
│       └── components/       # 公共组件
├── 启动后端.bat
├── 启动前端.bat
└── README.md
```

## 快速开始

### 1. 启动后端（Django）
双击运行 **`启动后端.bat`** 或手动执行：
```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations users vocabulary quiz progress
python manage.py migrate
python manage.py seed_words
python manage.py runserver 0.0.0.0:8000
```

### 2. 启动前端（Vue3）
双击运行 **`启动前端.bat`** 或手动执行：
```bash
cd frontend
npm install
npm run dev
```

### 3. 访问网站
- 前端地址：http://localhost:3000
- 后端 API：http://localhost:8000/api/v1/

## 功能特性

- 🔐 用户注册/登录（JWT 认证）
- 📖 词汇管理（按分类/难度浏览、搜索、收藏）
- 🃏 闪卡学习（翻卡记忆模式）
- 📝 多种测验（选择题/拼写题/英译中）
- 📊 学习进度追踪（打卡、统计、图表）
- 📱 响应式设计

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Django 4.2 + Django REST Framework |
| 认证 | Simple JWT |
| 数据库 | SQLite（文件存储于 backend/db/） |
| 前端框架 | Vue 3 (Composition API) |
| 路由 | Vue Router 4 |
| 状态管理 | Pinia |
| HTTP 客户端 | Axios |
| 构建工具 | Vite |

## 初始数据

运行 `seed_words` 命令后，系统包含 60 个英文单词，涵盖：
- 基础词汇（基础日常用语）
- 中级词汇（学术/工作用语）
- 高级词汇（GRE/托福水平）
- 商务词汇（职场英语）
- 旅游词汇（出行相关）
