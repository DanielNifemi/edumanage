# Docker Setup for EduManage

This document explains how to run the EduManage application using Docker.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose (included with Docker Desktop)

## Quick Start

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Build and start containers**:
   ```bash
   # Build containers
   docker-compose build

   # Start containers in detached mode
   docker-compose up -d
   ```

3. **Access the application**:
   - Backend (Django): http://localhost:8000
   - Frontend (React/Vite): http://localhost:3000
   - Database (PostgreSQL): localhost:5432

## Docker Services

The application consists of three main services:

### Web Service (Django Backend)
- **Port**: 8000
- **Image**: Custom built from Dockerfile
- **Database**: PostgreSQL
- **Auto-migrations**: Runs on startup
- **Superuser**: Creates admin/admin123 if not exists

### Database Service (PostgreSQL)
- **Port**: 5432
- **Database**: edumanage
- **Username**: edumanage_user
- **Password**: edumanage_password
- **Data**: Persisted in Docker volume

### Frontend Service (React/Vite)
- **Port**: 3000
- **Hot reload**: Enabled for development
- **API URL**: Points to backend at http://localhost:8000

## Useful Commands

### Using docker-compose directly:
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild containers
docker-compose build

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

### Using helper scripts:
```bash
# On Linux/Mac
./docker-helper.sh up
./docker-helper.sh logs
./docker-helper.sh migrate

# On Windows
docker-helper.bat up
docker-helper.bat logs
docker-helper.bat migrate
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django settings
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database settings
POSTGRES_DB=edumanage
POSTGRES_USER=edumanage_user
POSTGRES_PASSWORD=edumanage_password
DB_HOST=db
DB_PORT=5432

# CORS settings
CORS_ALLOW_ALL_ORIGINS=True
```

## Development Workflow

1. **Start development environment**:
   ```bash
   docker-compose up -d
   ```

2. **Make changes to code**: 
   - Backend changes will require container rebuild
   - Frontend changes are hot-reloaded automatically

3. **Run migrations after model changes**:
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

4. **Access Django admin**:
   - URL: http://localhost:8000/admin/
   - Username: admin
   - Password: admin123

## Troubleshooting

### Common Issues:

1. **Port already in use**:
   ```bash
   # Check what's using the port
   netstat -an | findstr :8000
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database connection errors**:
   ```bash
   # Restart database service
   docker-compose restart db
   ```

3. **Frontend not loading**:
   ```bash
   # Check frontend logs
   docker-compose logs frontend
   # Rebuild frontend container
   docker-compose build frontend
   ```

4. **Permission errors (Linux/Mac)**:
   ```bash
   # Make scripts executable
   chmod +x docker-helper.sh
   chmod +x docker-entrypoint.sh
   ```

### Reset Everything:
```bash
# Stop containers and remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## Production Considerations

When deploying to production:

1. Change `DEBUG=False` in environment
2. Use strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use environment-specific database credentials
5. Set up proper SSL/TLS certificates
6. Configure static file serving (nginx)
7. Use production-grade WSGI server (already using gunicorn)

## File Structure

```
├── Dockerfile                 # Django backend container
├── docker-compose.yml        # Multi-service configuration
├── docker-entrypoint.sh      # Backend startup script
├── .dockerignore             # Files to exclude from build
├── .env.example              # Environment template
├── docker-helper.sh          # Unix helper script
├── docker-helper.bat         # Windows helper script
└── frontend/
    └── Dockerfile            # Frontend container
```
