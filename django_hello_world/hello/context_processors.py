import django_hello_world.settings as conf


def settings(request):
    return {'settings': conf}