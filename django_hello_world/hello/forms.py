from django.forms import Form, ModelForm, DateField, ChoiceField
from models import Contact
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
    FIRST = '0'
    LAST = '1'
    EVENT_CHOICES = (
        (FIRST, 'First'),
        (LAST, 'Last'),
    )

    order = ChoiceField(EVENT_CHOICES, initial=FIRST, label='Ordering')