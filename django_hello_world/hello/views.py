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

    form = ContactForm(request.POST or None, request.FILES or None, instance=contact)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            return render(request, 'hello/form_edit.html', {
                'form': form,
                'contact': contact,
                'notification': 'Changes have been saved'
            })
        else:
            return HttpResponseRedirect(reverse('edit'))

    if request.is_ajax():
        return render(request, 'hello/form_edit.html', {'form': form, 'contact': contact})
    else:
        return render(request, 'hello/edit.html', {'form': form, 'contact': contact, 'log_request': log_request})