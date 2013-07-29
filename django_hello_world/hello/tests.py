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


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello!')

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