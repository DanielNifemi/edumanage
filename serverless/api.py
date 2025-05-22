from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumanage.settings')
application = get_wsgi_application()

def handler(request):
    return application(request)
