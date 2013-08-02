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


test_login = 'admin'
test_pwd = 'admin'


class HttpTest(TestCase):
    urls = 'django_hello_world.urls'

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/home.html')

    def test_edit(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=test_login, password=test_pwd)
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/edit.html')

    def test_requests(self):
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/requests.html')


class HomeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_data(self):
        response = self.client.get(reverse('home'))

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

        self.assertContains(response, response.context['contact'].email)

    def test_auth(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Login</a>')

        self.client.login(username=test_login, password=test_pwd)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Edit</a>')


class EditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=test_login, password=test_pwd)
        self.data_valid = {
            'email': 'abc@abc.com',
            'name': 'abc',
            'surname': 'qwe',
            'date_birth': '1981-11-11',
            'jabber': 'abc@abc.com',
            'skype': 'abc'
        }
        self.data_invalid = {
            'email': '.',
            'name': 'abc',
            'surname': 'qwe',
            'date_birth': '1981-11-11',
            'jabber': 'abc@abc.com',
            'skype': 'abc'
        }

    def test_form_view(self):
        response = self.client.get(reverse('edit'))
        self.assertIsNotNone(response.context['form'])
        self.assertContains(response, response.context['form'].fields['email'].label)

    def test_form_save(self):
        response = self.client.post(reverse('edit'), self.data_valid)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contact'].name, 'abc')

    def test_form_error(self):
        response = self.client.post(reverse('edit'), self.data_invalid)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid e-mail address')

    def test_form_ajax(self):
        response = self.client.post(reverse('edit'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/form_edit.html')
        self.assertIsNotNone(response.context['form'])
        self.assertContains(response, response.context['form'].fields['email'].label)


class MiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.middleware = RequestLoggerMiddleware()

    def test_log_write(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)
        self.assertEqual(LogRequest.objects.count(), 1)
        self.assertEqual(LogRequest.objects.get(pk=1).method, 'GET')
        self.assertEqual(LogRequest.objects.get(pk=1).path, '/')

    def test_log_not_write(self):
        request = self.factory.get(reverse('requests'))
        self.middleware.process_request(request)
        self.assertEqual(LogRequest.objects.count(), 0)

    def test_log_view(self):
        request = self.factory.get('/')
        self.middleware.process_request(request)

        response = self.client.get(reverse('requests'))
        self.assertIsNotNone(response.context['log_request'])
        self.assertContains(response, response.context['log_request'][0].host)
        self.assertIsNotNone(response.context['form'])
        self.assertContains(response, response.context['form'].fields['order'].label)

    def test_ordering(self):
        # add 2 records (id=1 and id=2)
        request = self.factory.get('/')
        self.middleware.process_request(request)
        self.middleware.process_request(request)

        response = self.client.get(reverse('requests'), {'order': LogOrderingForm.FIRST})
        self.assertEqual(response.context['log_request'][0].id, 1)

        response = self.client.get(reverse('requests'), {'order': LogOrderingForm.LAST})
        self.assertEqual(response.context['log_request'][0].id, 2)


class TemplateContextTest(TestCase):
    def test_enable(self):
        processor_result = settings(None)
        self.assertEqual(processor_result['settings'], conf)
        self.assertIn('django_hello_world.hello.context_processors.settings', conf.TEMPLATE_CONTEXT_PROCESSORS)


class TemplateTagsTest(TestCase):
    def test_work(self):
        self.assertEqual(edit_link(123), '()')
        self.assertEqual(edit_link(User.objects.get(pk=1)), '<a href="/admin/auth/user/1/">(admin)</a>')


class SignalsTest(TestCase):
    def _add_test_object(self):
        LogRequest.objects.create(
            host='localhost',
            path='/',
            method='GET',
        )

    def _edit_test_object(self):
        obj = LogRequest.objects.get(pk=1)
        obj.method = 'POST'
        obj.save()

    def _del_test_object(self):
        obj = LogRequest.objects.get(pk=1)
        obj.delete()

    def test_not_recursion(self):
        """
        Not reaction of LogModelSignals signals
        """
        post_save.connect(on_create_or_save)

        LogModelSignals.objects.create(
            model='test',
            event=LogModelSignals.CREATION,
        )
        self.assertEqual(LogModelSignals.objects.count(), 1)

        post_save.disconnect(on_create_or_save)

    def test_log_creation(self):
        post_save.connect(on_create_or_save)

        self._add_test_object()
        self.assertEqual(LogModelSignals.objects.count(), 1)
        self.assertEqual(LogModelSignals.objects.get(pk=1).event, LogModelSignals.CREATION)
        self.assertEqual(LogModelSignals.objects.get(pk=1).model, 'logrequest')

        post_save.disconnect(on_create_or_save)

    def test_log_editing(self):
        post_save.connect(on_create_or_save)

        self._add_test_object()
        self._edit_test_object()
        self.assertEqual(LogModelSignals.objects.count(), 2)
        self.assertEqual(LogModelSignals.objects.get(pk=2).event, LogModelSignals.EDITING)
        self.assertEqual(LogModelSignals.objects.get(pk=2).model, 'logrequest')

        post_save.disconnect(on_create_or_save)

    def test_log_deletion(self):
        post_save.connect(on_create_or_save)

        self._add_test_object()
        self._del_test_object()
        self.assertEqual(LogModelSignals.objects.count(), 2)
        self.assertEqual(LogModelSignals.objects.get(pk=2).event, LogModelSignals.DELETION)
        self.assertEqual(LogModelSignals.objects.get(pk=2).model, 'logrequest')

        post_save.disconnect(on_create_or_save)