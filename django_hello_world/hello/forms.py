from django.forms import ModelForm, DateField
from django.forms.extras.widgets import SelectDateWidget
from django_hello_world.hello.models import Contact


BIRTH_YEAR_CHOICES = ('1981', '1982', '1983', '1984', '1985')


class ContactForm(ModelForm):
    date_birth = DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))

    class Meta:
        model = Contact