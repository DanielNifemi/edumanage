# Docker Setup Guide

## Starting Docker Desktop
1. Open Docker Desktop application
2. Wait for it to fully start (Docker whale icon appears in system tray)
3. Ensure Docker Desktop shows "Engine running" status

## Running the Application
Once Docker Desktop is running, execute these commands:

```bash
# Navigate to project directory
cd /c/Users/USER/PycharmProjects/edumanage

# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

## Services that will start:
- **Database (PostgreSQL)**: Port 5432
- **Backend (Django)**: Port 8000
- **Frontend (Vite/React)**: Port 3000

## Accessing the Application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin (admin/admin123)

## Useful Commands:
```bash
# Stop all services
docker-compose down

# View logs
docker-compose logs

# View running containers
docker ps

# Rebuild specific service
docker-compose build web
docker-compose build frontend
```

## Troubleshooting:
If you get connection errors, ensure:
1. Docker Desktop is running
2. No other services are using ports 3000, 8000, or 5432
3. Windows Firewall allows Docker
