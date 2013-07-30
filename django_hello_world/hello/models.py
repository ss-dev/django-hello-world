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
    photo = models.ImageField('Photo', upload_to='photo', null=True)


class LogRequest(models.Model):
    date = models.DateTimeField('Datetime', auto_now_add=True)
    host = models.CharField('Host', max_length=150)
    path = models.CharField('Path', max_length=250)
    method = models.CharField('Method', max_length=30)