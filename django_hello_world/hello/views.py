from annoying.decorators import render_to
from django.contrib.auth.models import User
from models import Contact, LogRequest


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    contact = Contact.objects.get(pk=1)
    log_request = LogRequest.objects.filter().order_by('pk')[:10]
    return {'users': users, 'contact': contact, 'log_request': log_request}
