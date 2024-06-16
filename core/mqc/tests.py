from http import HTTPStatus
from django.test import RequestFactory, TestCase
from django.urls import reverse

class FaviconTests(TestCase):
    def test_get(self):
        response = self.client.get('/favicon.ico/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['Cache-Control'], 'max-age=86400, immutable, public')
        self.assertEqual(response['Content-Type'], 'image/x-icon')
        self.assertGreater(len(response.getvalue()), 0)

class DashboardViewTestCase(TestCase):
    def test_dashboard_view(self) -> None:
        response = self.client.get(reverse('mqc:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/mqc/dashboard.html')

class AdminViewTestCase(TestCase):
    def test_AdminView(self) -> None:
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, None)

class MajorQualityCaseListViewTestCase(TestCase):
    def test_MajorQualityCaseListView(self) -> None:
        response = self.client.get(reverse('mqc:dataset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/mqc/dataset.html')

# from unittest import mock

# class TestIceCreamSorting(TestCase):
#     @mock.patch.object(icecreamapi, 'get_flavors')
#     def test_flavor_sort(self, get_flavors):
#         get_flavors.return_value = ['chocolate', 'vanilla', 'strawberry', ]
#         flavors = list_flavors_sorted()
#         self.assertEqual(flavors, ['chocolate', 'strawberry', 'vanilla', ])

#     @mock.patch.object(icecreamapi, 'get_flavors')
#     def test_flavor_sort_failure(self, get_flavors):
#         # Instructs icecreamapi.get_flavors() to throw a FlavorError.
#         get_flavors.side_effect = icecreamapi.FlavorError()
#         # list_flavors_sorted() catches the icecreamapi.FlavorError()
#         # and passes on a CantListFlavors exception.
#         with self.assertRaises(CantListFlavors):
#             list_flavors_sorted()

#     @mock.patch.object(requests, 'get')
#     def test_request_failure(self, get):
#         """Test if the target site is inaccessible."""
#         get.side_effect = requests.exception.ConnectionError()
#         with self.assertRaises(CantListFlavors):
#             list_flavors_sorted()

#     @mock.patch.object(requests, 'get')
#     def test_request_failure_ssl(self, get):
#         """Test if we can handle SSL problems elegantly."""
#         get.side_effect = requests.exception.SSLError()
#         with self.assertRaises(CantListFlavors):
#             list_flavors_sorted()

# Form saves with all fields correctly filled using Django setup with the recommended fix
def test_form_saves_with_all_fields_correctly_filled_with_django_setup_fixed(self):
    import django
    from django.conf import settings
    django.setup()
    settings.configure()
    from django.forms.models import model_to_dict
    from .forms import MajorQualityCaseForm
    from .models import MajorQualityCase
    import datetime

    # Create a valid MajorQualityCase data dictionary
    valid_data = {
        '進捗': 50,
        '市場発生': True,
        '再発防止': False,
        '出荷停止': True,
        '責区': 1,  # Assuming ForeignKey id
        '責任者': 1,  # Assuming ForeignKey id
        'TAT': 'Test TAT',
        '製品分': 1,  # Assuming ForeignKey id
        '分類': 1,  # Assuming ForeignKey id
        '案件名': 'Test Case',
        '機種名型番': 'Model XYZ',
        '進捗状況': 'In progress',
        '発生場所': 1,  # Assuming ForeignKey id
        '発生日': datetime.date.today(),
        '不良症状内容': 'Defect details',
        '保留対象': 100,
        '依頼日': datetime.date.today(),
        '停止日': datetime.date.today(),
        '解除日': datetime.date.today(),
        '単品在庫': 500,
        '半製品在庫': 300,
        '完成品在庫': 200,
        '外部在庫': 150,
        '対応内容': 'Handling details',
        '実施予定日': datetime.date.today(),
        '実施実際日': datetime.date.today(),
        '実施部署': 1,  # Assuming ForeignKey id
        '実施者': 1,  # Assuming ForeignKey id
        '発生原因': 'Root cause analysis',
        '流出原因': 'Omission details',
        'なぜなぜ': 'Five whys analysis',
        '分析完了予定日': datetime.date.today(),
        '分析完了実際日': datetime.date.today(),
        '是正処置発生対策': 'Occurrence countermeasure',
        '是正処置流出対策': 'Omission countermeasure',
        '是正処置再発防止': 'Prevention countermeasure',
        '是正完了予定日': datetime.date.today(),
        '是正完了実際日': datetime.date.today(),
        'CLOSE日': datetime.date.today()
    }

    form = MajorQualityCaseForm(data=valid_data)
    assert form.is_valid(), f"Form should be valid. Errors: {form.errors}"
    instance = form.save()
    assert isinstance(instance, MajorQualityCase), "Should create a MajorQualityCase instance"

    # Form rejects non-date inputs for date fields with Django setup (Fixed)
def test_form_rejects_non_date_inputs_for_date_fields_with_django_setup_fixed(self):
    from django.conf import settings
    settings.configure()
    from .forms import MajorQualityCaseForm

    # Create a data dictionary with invalid date formats
    invalid_data = {
        '発生日': 'not-a-date',
        '依頼日': '2020-02-30',  # Invalid date
        '停止日': '2020-13-01',  # Invalid month
        '解除日': '',  # Empty string is not a valid date
    }

    form = MajorQualityCaseForm(data=invalid_data)
    assert not form.is_valid(), "Form should not be valid with non-date inputs for date fields"
    assert '発生日' in form.errors, "Should have error for invalid 発生日"
    assert '依頼日' in form.errors, "Should have error for invalid 依頼日"
    assert '停止日' in form.errors, "Should have error for invalid 停止日"
    assert '解除日' in form.errors, "Should have error for empty 解除日"