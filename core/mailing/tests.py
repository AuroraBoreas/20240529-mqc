from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SendMailViewTestCase(TestCase):
    def test_SendMailView(self) -> None:
        response = self.client.get(reverse('mailing:send'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, None)
