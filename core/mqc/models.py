import typing
import calendar
from collections import OrderedDict

from django.utils import timezone
from django.db.models.functions import ExtractMonth
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

from core.user.models import AppUser


class Department(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)    
    class Meta:
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['name'], name='department_name_idx'),
        ]
    def __str__(self) -> str:
        return self.name

class ResponsibilityCategory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'], name='respCategory_name_idx'),
        ]
    def __str__(self) -> str:
        return self.name
    
class PartCategory(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'PartCategories'
        indexes = [
            models.Index(fields=['name'], name='partCategory_name_idx'),
        ]
    def __str__(self) -> str:
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'Locations'
        indexes = [
            models.Index(fields=['name'], name='location_name_idx'),
        ]
    def __str__(self) -> str:
        return self.name

class DivisionCategory(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)
    class Meta:
        verbose_name_plural = 'DivisionCategories'
        indexes = [
            models.Index(fields=['name'], name='divisionCategory_name_idx'),
        ]
    def __str__(self) -> str:
        return self.name

import uuid as uuid_lib

class MajorQualityCase(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    progress = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        null=True,  blank=True, name='進捗'
    )
    market = models.BooleanField(null=True, default=False, name='市場発生')
    reoccurrence = models.BooleanField(null=True, default=False, name='再発防止')
    shipmentStop = models.BooleanField(null=True, default=False, name='出荷停止')
    responsibleCategory = models.ForeignKey(
        ResponsibilityCategory, on_delete=models.CASCADE,
        null=True, blank=False, name='責区',
    )
    responsibleUser = models.ForeignKey(
        AppUser, on_delete=models.CASCADE,
        null=True, blank=True, related_name='mqc_cases', name='責任者'
    )
    tat = models.CharField(max_length=255, null=False, blank=True, name='TAT')
    partCategory = models.ForeignKey(
        PartCategory, on_delete=models.CASCADE,
        null=True, blank=False, name='製品分'
    )
    divisionCategory = models.ForeignKey(
        DivisionCategory, on_delete=models.CASCADE,
        null=True, blank=False, name='分類'
    )
    caseName = models.CharField(max_length=255, null=False, blank=False, name='案件名')
    modelName = models.CharField(max_length=255, null=False, blank=False, name='機種名型番')
    progressDetail = models.TextField(null=True, blank=True, name='進捗状況')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE,
        null=True, blank=False, name='発生場所'
    )
    occurredAt = models.DateField(null=True, blank=True, name='発生日')
    defectSymptom = models.TextField(null=True, blank=True, name='不良症状内容')
    holdQty = models.PositiveBigIntegerField(null=False, blank=True, default=0, name='保留対象')
    receivedAt = models.DateField(null=True, blank=True, name='依頼日')
    stoppedAt = models.DateField(null=True, blank=True, name='停止日')
    releasedAt = models.DateField(null=True, blank=True, name='解除日')
    partStockQty = models.PositiveBigIntegerField(null=False, blank=True, default=0, name='単品在庫')
    wipStockQty = models.PositiveBigIntegerField(null=False, blank=True, default=0, name='半製品在庫')
    finishGoodStockQty = models.PositiveBigIntegerField(null=False, blank=True, default=0, name='完成品在庫')
    outerStockQty = models.PositiveBigIntegerField(null=False, blank=True, default=0, name='外部在庫')
    handlingContent = models.TextField(null=True, blank=True, name='対応内容')
    handlingPlanDate = models.DateField(null=True, blank=True, name='実施予定日')
    handlingActualDate = models.DateField(null=True, blank=True, name='実施実際日')
    handlingDepartment = models.ForeignKey(
        Department, on_delete=models.CASCADE,
        null=True, blank=True, name='実施部署'
    )
    handlingUser = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, 
        null=True, blank=True, related_name='handled_cases', name='実施者'
    )
    rootCause = models.TextField(null=True, blank=True, name='発生原因')
    omissionCause = models.TextField(null=True, blank=True, name='流出原因')
    analysisfiveWhy = models.TextField(null=True, blank=True, name='なぜなぜ')
    analysisPlanDate = models.DateField(null=True, blank=True, name='分析完了予定日')
    analysisActualDate = models.DateField(null=True, blank=True, name='分析完了実際日')
    occurrenceCounterMeasure = models.TextField(null=True, blank=True, name='是正処置発生対策')
    omissionCounterMeasure = models.TextField(null=True, blank=True, name='是正処置流出対策')
    preventionCounterMeasure = models.TextField(null=True, blank=True, name='是正処置再発防止')
    implementedPlanDate = models.DateField(null=True, blank=True, name='是正完了予定日')
    implementedActualDate = models.DateField(null=True, blank=True, name='是正完了実際日')
    caseClosedAt = models.DateField(null=True, blank=True, name='CLOSE日')
    file = models.FileField(null=True, blank=True, upload_to='uploads/')
    history = AuditlogHistoryField()

    def get_absolute_url(self) -> str:
        return reverse('mqc:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f'重大品質案件: {self.案件名}'
    
    @classmethod
    def get_qs(cls) -> models.manager.BaseManager:
        qs = MajorQualityCase.objects.prefetch_related(
            '責区',
            '責任者',
            '製品分',
            '分類',
            '発生場所',
            '実施部署',
            '実施者'
        )
        return qs
    
    class Meta:
        ordering = ['-発生日']
        indexes = [
            models.Index(fields=['発生日']),
            models.Index(fields=['分類']),
            models.Index(fields=['製品分']),
            models.Index(fields=['責区']),
            models.Index(fields=['実施部署']),
            models.Index(fields=['発生場所']),
        ]

auditlog.register(MajorQualityCase)

def get_dataset_per_month_of_current_year() -> dict[str, typing.Any]:
    current_year = timezone.datetime.now().year
    field = '発生日'
    try:
        objs = (
            MajorQualityCase
                .objects
                .values(field)
                .filter(
                    models.Q(発生日__isnull=False) & 
                    models.Q(発生日__year=current_year)
                )
                .annotate(month=ExtractMonth(field))
                .values('month')
                .annotate(n=models.Count(field))
                .order_by('month')
        )
        month_counts_dict = OrderedDict(zip(range(1,13), [0]*12))
        month_counts_dict.update(dict(objs.values_list('month','n')))
        labels = []
        data = []
        for k, v in month_counts_dict.items():
            labels.append(calendar.month_abbr[k])
            data.append(v)
        category = 'Month'
        context = {
            'type'  : 'bar',
            'labels': list(labels),
            'data'  : list(data),
            'label' : f'# per {category}',
            'title' : f'Major Quality Case per {category} in {current_year}',
        }
        return context
    except MajorQualityCase.DoesNotExist:
        return EMPTY_CONTEXT

def generate_labels_and_data(
    qs: models.QuerySet,
    f: str,
    g: str='n'
) -> tuple[list[str],list[int|float]]:
    labels = []
    data = []
    for q in qs:
        labels.append(q[f])
        data.append(q[g])
    return labels,data

def generate_context(qs: models.QuerySet, c: str, t: str='bar') -> dict[str, typing.Any]:
    labels, data = generate_labels_and_data(qs, c)
    context = {
        'type'  : t,
        'labels': list(labels),
        'data'  : list(data),
        'label' : f'# of {c.title()}',
        'title' : f'Major Quality Case per {c.title()}',
    }
    return context

EMPTY_CONTEXT = {
    'type'  : None,
    'labels': list(),
    'data'  : list(),
    'label' : f'# of {None}',
    'title' : f'Major Quality Case per {None}',
}

def get_dataset_per_division() -> dict[str, typing.Any]:
    field = '分類__name'
    try:
        objs = (
            MajorQualityCase
                .objects
                .values(field)
                .filter(models.Q(分類__isnull=False))
                .annotate(
                    division=models.F(field),
                    n=models.Count(field)
                )
        )
        return generate_context(objs, 'division', t='pie')
    except MajorQualityCase.ObjectDoesNotExist:
        return EMPTY_CONTEXT

def get_dataset_per_partCategory() -> dict[str, typing.Any]:
    field = '製品分__name'
    try:
        objs = (
            MajorQualityCase.objects
                .values(field)
                .filter(models.Q(製品分__isnull=False))
                .annotate(
                    part=models.F(field),
                    n=models.Count(field)
                )
        )
        return generate_context(objs, 'part', t='doughnut')
    except MajorQualityCase.ObjectDoesNotExist:
        return EMPTY_CONTEXT

def get_dataset_per_responsibility() -> dict[str, typing.Any]:
    field = '責区__name'
    try:
        objs = (
            MajorQualityCase.objects
                .values(field)
                .filter(models.Q(責区__isnull=False))
                .annotate(
                    responsibility=models.F(field),
                    n=models.Count(field)
                )
        )
        return generate_context(objs, 'responsibility', t='radar')
    except MajorQualityCase.ObjectDoesNotExist:
        return EMPTY_CONTEXT

def get_dataset_per_department() -> dict[str, typing.Any]:
    field = '実施部署__name'
    try:
        objs = (
            MajorQualityCase.objects
                .values(field)
                .filter(models.Q(実施部署__isnull=False))
                .annotate(
                    department=models.F(field),
                    n=models.Count(field)
                )
        )
        return generate_context(objs, 'department', t='polarArea')
    except MajorQualityCase.ObjectDoesNotExist:
        return EMPTY_CONTEXT

def get_dataset_per_location() -> dict[str, typing.Any]:
    field = '発生場所__name'
    try:
        objs = (
            MajorQualityCase.objects
                .values(field)
                .filter(models.Q(発生場所__isnull=False))
                .annotate(
                    location=models.F(field),
                    n=models.Count(field)
                )
        )
        return generate_context(objs, 'location')
    except MajorQualityCase.ObjectDoesNotExist:
        return EMPTY_CONTEXT
