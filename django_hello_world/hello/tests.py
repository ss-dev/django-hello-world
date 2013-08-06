from io import StringIO
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User
from django.core.management import call_command
from models import LogRequest, LogModelSignals
from middleware import RequestLoggerMiddleware
from context_processors import settings
from templatetags.hello_tags import edit_link
from forms import LogOrderingForm
import django_hello_world.settings as conf

from django.db.models.signals import post_save
from signal_receivers import on_create_or_save
post_save.disconnect(on_create_or_save)


TEST_LOGIN = 'admin'
TEST_PWD = 'admin'


class HttpTest(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/home.html')

    def test_edit(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=TEST_LOGIN, password=TEST_PWD)
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/edit.html')

    def test_requests(self):
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/requests.html')


class HomeTest(TestCase):
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

        self.client.login(username=TEST_LOGIN, password=TEST_PWD)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Edit</a>')


class EditTest(TestCase):
    def setUp(self):
        self.client.login(username=TEST_LOGIN, password=TEST_PWD)
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


class RequestsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestLoggerMiddleware()

        request = self.factory.get('/')
        self.middleware.process_request(request)

        self.data_valid = {
            'form-0-id': '1',
            'form-0-priority': '123',
            'form-INITIAL_FORMS': 1,
            'form-MAX_NUM_FORMS': 1000,
            'form-TOTAL_FORMS': 1
        }
        self.data_invalid = {
            'form-0-id': '1',
            'form-0-priority': 'abc',
            'form-INITIAL_FORMS': 1,
            'form-MAX_NUM_FORMS': 1000,
            'form-TOTAL_FORMS': 1
        }

    def test_log_view(self):
        response = self.client.get(reverse('requests'))
        self.assertIsNotNone(response.context['formset'])
        self.assertContains(response, response.context['formset'][0].instance.host)
        self.assertIsNotNone(response.context['form'])
        self.assertContains(response, response.context['form'].fields['order'].label)

    def test_ordering(self):
        # add 2 records (id=2, priority=100)
        request = self.factory.get('/')
        self.middleware.process_request(request)
        obj = LogRequest.objects.get(pk=2)
        obj.priority = 100
        obj.save()

        response = self.client.get(reverse('requests'), {'order': LogOrderingForm.DATE})
        self.assertEqual(response.context['formset'][0].instance.id, 1)

        response = self.client.get(reverse('requests'), {'order': LogOrderingForm.PRIORITY})
        self.assertEqual(response.context['formset'][0].instance.id, 2)

    def test_formset_save(self):
        response = self.client.post(reverse('requests'), self.data_valid)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['formset'][0].instance.priority, 123)

    def test_formset_error(self):
        response = self.client.post(reverse('requests'), self.data_invalid)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a whole number')


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


class CommandTest(TestCase):
    def test_models_info(self):
        out = StringIO()
        err = StringIO()
        call_command('models_info', stdout=out, stderr=err)
        self.assertTrue(out.getvalue().find('user - 1') >= 0)
        self.assertTrue(err.getvalue().find('error: user - 1') >= 0)