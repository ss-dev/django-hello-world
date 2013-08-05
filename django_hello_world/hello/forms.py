from django.forms import Form, ModelForm, DateField, ChoiceField
from django.forms.models import modelformset_factory
from models import Contact, LogRequest
from widgets import DatePickerWidget


class ContactForm(ModelForm):
    date_birth = DateField(widget=DatePickerWidget(
        params="""changeMonth: true, changeYear: true,
            dateFormat: 'yy-mm-dd', yearRange: 'c-40:c+1'""",
        attrs={'class': 'datepicker', }
    ))

    class Meta:
        model = Contact


class LogOrderingForm(Form):
    DATE = '0'
    PRIORITY = '1'
    SORT_CHOICES = (
        (DATE, 'date'),
        (PRIORITY, 'priority'),
    )

    order = ChoiceField(SORT_CHOICES, initial=DATE, label='Sorting by')


LogRequestFormSet = modelformset_factory(LogRequest, fields=('priority',), extra=0)