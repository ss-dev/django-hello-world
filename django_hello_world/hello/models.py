from django.db import models


class Contact(models.Model):
    name = models.CharField('Name', max_length=20)
    surname = models.CharField('Last name', max_length=20)
    date_birth = models.DateField('Date of birth')
    email = models.EmailField('Email')
    jabber = models.EmailField('Jabber')
    skype = models.CharField('Skype', max_length=20)
    contacts = models.TextField('Other contacts')
    bio = models.TextField('Bio')