@echo off
echo Starting EduManage with Docker...
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Docker is not running or not installed.
    echo Please install Docker Desktop and make sure it's running.
    echo Download from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo Docker is available. Building and starting containers...
echo.

REM Stop any existing containers
docker-compose down

REM Build and start the containers
docker-compose up --build

pause
