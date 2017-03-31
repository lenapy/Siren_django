from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from siren_proj.user.forms import RegistrationForm, LoginForm, PasswordChangeForm
from siren_proj.models import User


class TestRegistrationUser(TestCase):

    def test_registration_form_not_valid(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())

    def test_registration_form_valid(self):
        form = RegistrationForm(data={'login': 'test_login',
                                      'password': 'test_password',
                                      'username': 'test_name',
                                      'mail_address': 'test@test.com'})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_registration_view_redirect(self):
        response = user_registration()
        self.assertEqual(response.status_code, 302)

    def test_registration_view_user_exist(self):
        expected_login = 'test_login'
        user_registration()
        self.assertTrue(User.objects.filter(login=expected_login).first())


def user_registration():
    c = Client()
    return c.post(reverse('user:registration'), data={
        'login': 'test_login',
        'password': 'test_password',
        'username': 'test_name',
        'mail_address': 'test@test.com'})


class TestLogInUser(TestCase):

    def test_login_form_not_valid(self):
        form = LoginForm(data={'login': 'fake',
                               'password': 'fake_password'})
        self.assertFalse(form.is_valid())

    def test_login_view_ok(self):
        c = Client()
        user_registration()
        response = c.post(reverse('user:login'), data={'login': 'test_login',
                                                       'password': 'test_password'})
        self.assertEqual(response.status_code, 302)

    def test_login_view_invalid_data(self):
        c = Client()
        user_registration()
        response = c.post(reverse('user:login'), data={'login': 'invalid_log',
                                                       'password': 'invalid_passw'})
        self.assertEqual(response.status_code, 200)


class TestLogOutUser(TestCase):

    def test_logout_ok(self):
        c = Client()
        user_registration()
        c.post(reverse('user:login'), data={'login': 'test_login',
                                            'password': 'test_password'})
        response = c.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)


class TestChangePassword(TestCase):
    def test_change_password_form_valid(self):
        user_registration()
        form = PasswordChangeForm(data={'password': 'test_password',
                                        'new_password': 'test_new_password',
                                        'reenter_password': 'test_new_password',
                                        })
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_change_password_form_new_pass_equal_pass(self):
        user_registration()
        PasswordChangeForm(data={'password': 'test_password',
                                 'new_password': 'test_password',
                                 'reenter_password': 'test_password',
                                 })
        self.assertRaises(forms.ValidationError)

    def test_change_password_form_new_pass_not_equal_reenter_pass(self):
        user_registration()
        PasswordChangeForm(data={'password': 'test_password',
                                 'new_password': 'new_password',
                                 'reenter_password': 'some_password',
                                 })
        self.assertRaises(forms.ValidationError)

