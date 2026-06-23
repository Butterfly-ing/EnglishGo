@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ========================================
echo   EnglishGo - 启动 Vue3 前端服务
echo ========================================
echo.

cd /d "%~dp0frontend"

:: 检测 Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)
echo [✓] Node.js 已检测到

:: 检测 npm / 或 pnpm
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 npm
    pause
    exit /b 1
)

:: 安装依赖
if not exist "node_modules" (
    echo [1/3] 安装依赖（首次可能较慢）...
    call npm install
    if %errorlevel% neq 0 (
        echo [错误] npm install 失败，请检查网络或 Node 版本
        pause
        exit /b 1
    )
    echo [✓] 依赖安装完成
) else (
    echo [1/3] node_modules 已存在，跳过安装
)

:: 检查端口
echo [2/3] 检查端口占用...
netstat -ano | findstr ":3000" >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 端口 3000 已被占用，将尝试继续启动（可能自动切换到其他端口）
) else (
    echo [✓] 端口 3000 空闲
)

:: 启动开发服务器
echo.
echo ========================================
echo  [3/3] 启动前端开发服务器...
echo  前端地址: http://localhost:3000
echo  后端 API 代理: /api/v1 ^-^> http://localhost:8000
echo  按 Ctrl+C 停止服务器
echo ========================================
echo.
call npm run dev

pause
