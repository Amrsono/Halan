@echo off
REM Quick Start Script for Halan Invest (Windows)

echo.
echo 🚀 Halan Invest - Quick Start
echo ==============================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker found

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Desktop (includes Compose).
    pause
    exit /b 1
)

echo ✅ Docker Compose found

REM Create .env if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from .env.example...
    copy .env.example .env
    echo ✅ .env created
) else (
    echo ✅ .env already exists
)

REM Start services
echo.
echo 🐳 Starting Docker services...
docker-compose up -d

REM Wait for services to be ready
echo.
echo ⏳ Waiting for services to start (15 seconds)...
timeout /t 15

REM Check if services are running
echo.
echo 🔍 Checking services...
docker-compose ps

REM Print access information
echo.
echo ✅ All services started!
echo.
echo 📊 Dashboard: http://localhost:3000
echo 📡 API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo View logs with: docker-compose logs -f
echo Stop services with: docker-compose down
echo.
pause
