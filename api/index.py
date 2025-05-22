from edumanage.wsgi import application

def handler(request, **kwargs):
    return application(request, **kwargs)
