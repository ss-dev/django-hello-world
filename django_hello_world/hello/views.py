from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import Contact, LogRequest


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    contact = Contact.objects.get(pk=1)
    log_request = LogRequest.objects.filter().order_by('pk')[:10]
    return {'users': users, 'contact': contact, 'log_request': log_request}


@login_required()
@render_to('hello/home.html')
def edit(request):
    pass