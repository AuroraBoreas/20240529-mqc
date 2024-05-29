from core.mqc.models import (
    Department,
    ResponsibilityCategory,
    PartCategory,
    Location,
    DivisionCategory,
    MajorQualityCase,
)

from django.contrib.auth.models import Group
from django.db import connection
from pprint import pprint
from django.db.models import Count, Value, F, Q
from django.db.models.functions import ExtractMonth, TruncMonth
import calendar
from django.utils import timezone
from collections import OrderedDict

from core.user.models import AppUser


def run() -> None:
    # field = '責区__name'
    # objs = (
    #     MajorQualityCase.objects
    #         .filter(責区__isnull=False)
    #         .values(field)
    #         .annotate(
    #             product=F(field),
    #             n=Count('pk')
    #         )
    # )
    # print(objs)

    # current_year = timezone.datetime.now().year
    # field = '発生日'
    # try:
    #     objs = (
    #         MajorQualityCase
    #             .objects
    #             .values(field)
    #             .filter(
    #                 Q(発生日__isnull=False) & 
    #                 Q(発生日__year=current_year)
    #             )
    #             .annotate(month=ExtractMonth(field))
    #             .values('month')
    #             .annotate(n=Count(field))
    #             .order_by('month')
    #     )
    # except MajorQualityCase.DoesNotExist:
    #     msg = 'there is no records of {0}'.format(field)
    #     raise ValueError(msg)
    
    # month_counts_dict = OrderedDict(zip(range(1,13),[0]*12))
    # month_counts_dict.update(dict(objs.values_list('month','n')))
    # labels = []
    # data = []
    # for k, v in month_counts_dict.items():
    #     labels.append(calendar.month_abbr[k])
    #     data.append(v)

    # field = '分類__name'
    # objs = (
    #     MajorQualityCase
    #         .objects
    #         .values(field)
    #         .filter(Q(分類__isnull=False))
    #         .annotate(
    #             division=F(field),
    #             n=Count(field)
    #         )
    # )
    # labels = []
    # data = []
    # for obj in objs:
    #     labels.append(obj['division'])
    #     data.append(obj['n'])
    # labels = objs.values_list('division', flat=True)
    # data = objs.values_list('n', flat=True)

    # print(objs)

    # field = '製品分__name'
    # objs = (
    #     MajorQualityCase.objects
    #         .filter(Q(製品分__isnull=False))
    #         .values(field)
    #         .annotate(
    #             part=F(field),
    #             n=Count(field)
    #         )
    # )
    # data = list(objs.values_list('part','n'))
    # labels = objs.values_list('part', flat=True)
    # data = objs.values_list('n', flat=True)

    # print('labels:', labels)
    # print('data:', data)
    
    # objs = MajorQualityCase.objects.prefetch_related(
    #     '責区',
    #     '責任者',
    #     '製品分',
    #     '分類',
    #     '発生場所',
    #     '実施部署',
    #     '実施者'
    # ).first()

    
    
    # print(objs)
    objs = Group.objects.first()
    # prefetch_related('AppUser').first()
    print(f'{objs=}')

    from django.utils.translation import gettext_lazy
    pprint(connection.queries)
