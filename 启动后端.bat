@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   EnglishGo - 启动 Django 后端服务
echo ========================================
echo.

cd /d "%~dp0backend"

:: 检测 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)
echo [✓] Python 已检测到

:: 创建虚拟环境（如不存在）
if not exist "venv" (
    echo [1/5] 创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo [✓] 虚拟环境创建完成
) else (
    echo [1/5] 虚拟环境已存在，跳过创建
)

:: 激活虚拟环境并安装依赖
echo [2/5] 安装 Python 依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo [警告] 清华源失败，尝试默认源...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)
echo [✓] 依赖安装完成

:: 执行迁移
echo [3/6] 执行数据库迁移...
python manage.py makemigrations users vocabulary quiz progress articles
python manage.py migrate
if %errorlevel% neq 0 (
    echo [错误] 数据库迁移失败
    pause
    exit /b 1
)
echo [✓] 数据库迁移完成

:: 导入初始词汇
echo [4/6] 导入初始词汇数据...
python manage.py seed_words
if %errorlevel% neq 0 (
    echo [警告] 初始词汇导入失败（可能已存在）
)

:: 导入初始文章
echo [5/6] 导入初始文章数据...
python manage.py seed_articles
if %errorlevel% neq 0 (
    echo [警告] 初始文章导入失败（可能已存在）
)
echo [✓] 数据初始化完成

:: 启动服务器
echo.
echo ========================================
echo  [6/6] 启动开发服务器...
echo  后端地址: http://localhost:8000
echo  API 基础路径: http://localhost:8000/api/v1/
echo  按 Ctrl+C 停止服务器
echo ========================================
echo.
python manage.py runserver 0.0.0.0:8000

pause
