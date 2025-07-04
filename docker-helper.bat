@echo off

if "%1"=="build" (
    echo Building Docker containers...
    docker-compose build
) else if "%1"=="up" (
    echo Starting Docker containers...
    docker-compose up -d
) else if "%1"=="down" (
    echo Stopping Docker containers...
    docker-compose down
) else if "%1"=="logs" (
    echo Showing logs...
    docker-compose logs -f
) else if "%1"=="shell" (
    echo Opening Django shell...
    docker-compose exec web python manage.py shell
) else if "%1"=="migrate" (
    echo Running migrations...
    docker-compose exec web python manage.py migrate
) else if "%1"=="createsuperuser" (
    echo Creating superuser...
    docker-compose exec web python manage.py createsuperuser
) else if "%1"=="restart" (
    echo Restarting Docker containers...
    docker-compose down
    docker-compose up -d
) else (
    echo Usage: %0 {build^|up^|down^|logs^|shell^|migrate^|createsuperuser^|restart}
    echo.
    echo Commands:
    echo   build          - Build Docker containers
    echo   up             - Start Docker containers
    echo   down           - Stop Docker containers
    echo   logs           - Show container logs
    echo   shell          - Open Django shell
    echo   migrate        - Run database migrations
    echo   createsuperuser - Create Django superuser
    echo   restart        - Restart all containers
)
