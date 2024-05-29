from django.test import TestCase
from django.urls import reverse

class RegisterViewTestCase(TestCase):
    def test_RegisterView(self) -> None:
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/register.html')

class LoginViewTestCase(TestCase):
    def test_LoginView(self) -> None:
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/user/login.html')

class LogoutViewTestCase(TestCase):
    def test_LogoutView(self) -> None:
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, None)
