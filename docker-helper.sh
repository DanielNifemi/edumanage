#!/bin/bash

# Docker management script for edumanage project

case "$1" in
    "build")
        echo "Building Docker containers..."
        docker-compose build
        ;;
    "up")
        echo "Starting Docker containers..."
        docker-compose up -d
        ;;
    "down")
        echo "Stopping Docker containers..."
        docker-compose down
        ;;
    "logs")
        echo "Showing logs..."
        docker-compose logs -f
        ;;
    "shell")
        echo "Opening Django shell..."
        docker-compose exec web python manage.py shell
        ;;
    "migrate")
        echo "Running migrations..."
        docker-compose exec web python manage.py migrate
        ;;
    "createsuperuser")
        echo "Creating superuser..."
        docker-compose exec web python manage.py createsuperuser
        ;;
    "restart")
        echo "Restarting Docker containers..."
        docker-compose down
        docker-compose up -d
        ;;
    *)
        echo "Usage: $0 {build|up|down|logs|shell|migrate|createsuperuser|restart}"
        echo ""
        echo "Commands:"
        echo "  build          - Build Docker containers"
        echo "  up             - Start Docker containers"
        echo "  down           - Stop Docker containers"
        echo "  logs           - Show container logs"
        echo "  shell          - Open Django shell"
        echo "  migrate        - Run database migrations"
        echo "  createsuperuser - Create Django superuser"
        echo "  restart        - Restart all containers"
        exit 1
        ;;
esac
