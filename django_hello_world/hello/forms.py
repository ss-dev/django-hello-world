from django.forms import ModelForm, DateField
from django_hello_world.hello.models import Contact
from django_hello_world.hello.widgets import DatePickerWidget


class ContactForm(ModelForm):
    date_birth = DateField(widget=DatePickerWidget(
        params="""changeMonth: true, changeYear: true,
            dateFormat: 'yy-mm-dd', yearRange: 'c-40:c+1'""",
        attrs={'class': 'datepicker', }
    ))

    class Meta:
        model = Contact