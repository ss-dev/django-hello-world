from django.db import models


class Contact(models.Model):
    name = models.CharField('Name', max_length=20)
    surname = models.CharField('Last name', max_length=20)
    date_birth = models.DateField('Date of birth')
    email = models.EmailField('Email')
    jabber = models.EmailField('Jabber')
    skype = models.CharField('Skype', max_length=20)
    contacts = models.TextField('Other contacts', blank=True)
    bio = models.TextField('Bio', blank=True)
    photo = models.ImageField('Photo', upload_to='photo', blank=True, null=True)


class LogRequest(models.Model):
    date = models.DateTimeField('Datetime', auto_now_add=True)
    host = models.CharField('Host', max_length=150)
    path = models.CharField('Path', max_length=250)
    method = models.CharField('Method', max_length=30)
    priority = models.IntegerField('Priority', blank=True, default=0)

    class Meta:
        ordering = ['date']


class LogModelSignals(models.Model):
    CREATION = 'C'
    EDITING = 'E'
    DELETION = 'D'
    EVENT_CHOICES = (
        (CREATION, 'Creation'),
        (EDITING, 'Editing'),
        (DELETION, 'Deletion'),
    )

    date = models.DateTimeField('Datetime', auto_now_add=True)
    model = models.CharField('Model', max_length=100)
    event = models.CharField('Event', max_length=1, choices=EVENT_CHOICES)