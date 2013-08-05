from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from models import Contact, LogRequest
from forms import ContactForm, LogRequestFormSet, LogOrderingForm


@render_to('hello/home.html')
def home(request):
    contact = Contact.objects.get(pk=1)
    return {'contact': contact}


@render_to('hello/requests.html')
@csrf_protect
def requests(request):
    form = LogOrderingForm(request.GET or None)
    if form.is_valid() and form.cleaned_data['order'] == LogOrderingForm.PRIORITY:
        insts = LogRequest.objects.filter().order_by('-priority')[:10]
    else:
        insts = LogRequest.objects.filter()[:10]

    formset = LogRequestFormSet(request.POST or None, queryset=insts)

    if formset.is_valid():
        formset.save()
        return HttpResponseRedirect(reverse('requests'))

    return {'formset': formset, 'form': form}


@login_required()
@csrf_protect
def edit(request):
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
        return render(request, 'hello/edit.html', {'form': form, 'contact': contact})