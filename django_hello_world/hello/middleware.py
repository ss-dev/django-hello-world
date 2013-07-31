from django.core.urlresolvers import reverse, resolve
from django_hello_world.hello.models import LogRequest


class RequestLoggerMiddleware(object):
    def process_request(self, request):
        if resolve(request.path).url_name != 'requests':
            LogRequest.objects.create(
                host=request.get_host(),
                path=request.path,
                method=request.method,
            )