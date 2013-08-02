"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
import django_hello_world.settings as conf
from models import LogRequest, LogModelSignals
from middleware import RequestLoggerMiddleware
from context_processors import settings
from templatetags.hello_tags import edit_link
from forms import LogOrderingForm

from django.db.models.signals import post_save
from signals import on_create_or_save
post_save.disconnect(on_create_or_save)


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assignment')
        self.assertContains(response, 'Login</a>')

        response = c.get(reverse('edit'))
        self.assertNotEqual(response.status_code, 200)

        c.login(username='admin', password='admin')
        response = c.get(reverse('home'))
        self.assertContains(response, 'Edit</a>')

    def test_contact(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['contact'])
        self.assertIsNotNone(response.context['contact'].name)
        self.assertIsNotNone(response.context['contact'].surname)
        self.assertIsNotNone(response.context['contact'].date_birth)
        self.assertIsNotNone(response.context['contact'].email)
        self.assertIsNotNone(response.context['contact'].jabber)
        self.assertIsNotNone(response.context['contact'].skype)
        self.assertIsNotNone(response.context['contact'].contacts)
        self.assertIsNotNone(response.context['contact'].bio)
        self.assertIsNotNone(response.context['contact'].photo)

    def test_edit(self):
        c = Client()
        response = c.get(reverse('edit'))
        self.assertNotEqual(response.status_code, 200)

        c.login(username='admin', password='admin')
        response = c.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

        data = {
            'name': 'abc',
            'surname': 'qwe',
            'date_birth': '1981-11-11',
            'email': 'abc@abc.com',
            'jabber': 'abc@abc.com',
            'skype': 'abc'
        }
        c.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)

        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contact'].name, 'abc')

        data['email'] = '.'
        response = c.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid e-mail address')

        response = c.get(reverse('edit'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

    def test_middleware_request_logger(self):
        factory = RequestFactory()
        request = factory.get('/')
        middleware = RequestLoggerMiddleware()
        middleware.process_request(request)

        self.assertEqual(LogRequest.objects.count(), 1)
        self.assertEqual(LogRequest.objects.get(pk=1).method, 'GET')
        self.assertEqual(LogRequest.objects.get(pk=1).path, '/')

        request = factory.get(reverse('requests'))
        middleware.process_request(request)
        self.assertEqual(LogRequest.objects.count(), 1)

        c = Client()
        response = c.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'requests')
        self.assertIsNotNone(response.context['log_request'])

    def test_template_context(self):
        processor_result = settings(None)
        self.assertEqual(processor_result['settings'], conf)
        self.assertIn('django_hello_world.hello.context_processors.settings', conf.TEMPLATE_CONTEXT_PROCESSORS)

    def test_template_tags(self):
        self.assertEqual(edit_link(123), '()')
        self.assertEqual(edit_link(User.objects.get(pk=1)), '<a href="/admin/auth/user/1/">(admin)</a>')

    def test_model_signals(self):
        post_save.connect(on_create_or_save)

        c = Client()
        c.get(reverse('requests'))
        self.assertEqual(LogModelSignals.objects.count(), 0)

        c.get(reverse('home'))
        self.assertEqual(LogModelSignals.objects.count(), 1)
        self.assertEqual(LogModelSignals.objects.get(pk=1).event, LogModelSignals.CREATION)
        self.assertEqual(LogModelSignals.objects.get(pk=1).model, 'logrequest')

        post_save.disconnect(on_create_or_save)


class HttpTest2(TestCase):
    fixtures = ['log_requests']

    def test_ordering_requests(self):
        c = Client()
        response = c.get(reverse('requests'), {'order': LogOrderingForm.FIRST})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])
        self.assertIsNotNone(response.context['log_request'])
        self.assertEqual(response.context['log_request'][0].id, 1)

        response = c.get(reverse('requests'), {'order': LogOrderingForm.LAST})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])
        self.assertIsNotNone(response.context['log_request'])
        self.assertEqual(response.context['log_request'][0].id, 2)