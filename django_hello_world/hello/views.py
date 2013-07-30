from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from models import Contact, LogRequest
from forms import ContactForm


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    contact = Contact.objects.get(pk=1)
    log_request = LogRequest.objects.filter().order_by('pk')[:10]
    return {'users': users, 'contact': contact, 'log_request': log_request}


@login_required()
@csrf_protect
def edit(request):
    log_request = LogRequest.objects.filter().order_by('pk')[:10]
    contact = Contact.objects.get(pk=1)

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('edit'))
    else:
        form = ContactForm(instance=contact)

    return render(request, 'hello/edit.html', {'form': form, 'log_request': log_request})