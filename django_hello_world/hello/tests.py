"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django_hello_world.hello.models import LogRequest
from django_hello_world.hello.middleware import RequestLoggerMiddleware
from django_hello_world.hello.context_processors import settings
import django_hello_world.settings as conf


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '42 Coffee Cups Test Assignment')
        self.assertContains(response, 'Login</a>')

        response = c.get(reverse('edit'))
        self.assertNotEqual(response.status_code, 200)

        c.post('/login/', {'username': 'admin', 'password': 'admin'})
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

        c.post('/login/', {'username': 'admin', 'password': 'admin'})
        response = c.get(reverse('edit'))
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

        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'requests')
        self.assertIsNotNone(response.context['log_request'])

    def test_template_context(self):
        processor_result = settings(None)
        self.assertEqual(processor_result['settings'], conf)
        self.assertIn('django_hello_world.hello.context_processors.settings', conf.TEMPLATE_CONTEXT_PROCESSORS)
