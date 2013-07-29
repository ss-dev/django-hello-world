from annoying.decorators import render_to
from django.contrib.auth.models import User
from models import Contact


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    contact = Contact.objects.get(pk=1)
    return {'users': users, 'contact': contact}
