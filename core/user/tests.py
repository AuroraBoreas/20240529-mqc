from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse


class AppUserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.User = get_user_model()
        cls.User.objects.create(
            email='username1@domain.com',
            username='username1',
            password='password123',
        )

    def setUp(self) -> None:
        self.test_instance = self.User.objects.get(username='username1')
    
    def test_model_creation(self) -> None:
        self.assertEqual(self.test_instance.email, 'username1@domain.com')

    def test_model_authentication(self) -> None:
        self.assertEqual(self.test_instance.password, 'password123')
        self.assertTrue(self.test_instance.is_active)
        self.assertFalse(self.test_instance.is_staff)
        self.assertTrue(self.test_instance.is_authenticated)
        self.assertFalse(self.test_instance.is_anonymous)

    def test_model_update_username(self) -> None:
        new_username = 'username2'
        self.test_instance.username = new_username
        self.test_instance.save()
        updated_user = self.User.objects.get(username=new_username)
        self.assertEqual(updated_user.username, new_username)

    def test_model_deletion(self) -> None:
        self.test_instance.delete()
        self.assertFalse(self.User.objects.filter(username='username1').exists())

class AppUserRegisterViewTests(TestCase):
    def setUp(self):
        url = reverse('user:register')
        self.response = self.client.get(url)

    def test_AppUser_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_AppUser_template(self) -> None:
        self.assertTemplateUsed(self.response, 'core/user/register.html')
        self.assertContains(self.response, 'Join Today')
        self.assertNotContains(self.response, 'Join Tonight')

    def test_AppUser_url_resolves_AppUser(self) -> None:
        from . import views
        view = resolve('/user/register/')
        self.assertEqual(view.func.__name__, views.register.__name__)

    def test_AppUser_AppUserRegisterForm(self) -> None:
        from .forms import AppUserRegisterForm
        form = self.response.context.get('form')
        self.assertIsInstance(form, AppUserRegisterForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

class AppUserLoginViewTests(TestCase):
    def setUp(self):
        url = reverse('user:login')
        self.response = self.client.get(url)

    def test_AppUser_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_AppUser_template(self) -> None:
        self.assertTemplateUsed(self.response, 'core/user/login.html')
        self.assertContains(self.response, 'Login')
        self.assertNotContains(self.response, 'Logout')

    def test_AppUser_url_resolves_AppUser(self) -> None:
        from . import views
        view = resolve('/user/login/')

from django.test import Client

class AppUserLogoutViewTests(TestCase):
    def setUp(self) -> None:
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create(
            username='testuser',
            email='test.email@domain.com',
            password='testpass'
        )
        self.client = Client()
        self.client.login(email='test.email@domain.com', password='testpass')
        self.response = self.client.get(reverse('user:logout'))

    def test_AppUser_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 302)

    def test_AppUser_template(self) -> None:
        self.assertTemplateNotUsed(self.response, 'core/user/logout.html')

    def test_AppUser_url_resolves_AppUser(self) -> None:
        from . import views
        view = resolve('/user/logout/')
        self.assertEqual(view.func.__name__, views.logout.__name__)
