import django_filters
from django_filters.widgets import RangeWidget
from .models import MajorQualityCase

class MajorQualityCaseFilter(django_filters.FilterSet):
    """
    Filter class for filtering MajorQualityCase objects based on various fields.

    Attributes:
        model: The MajorQualityCase model to filter.
        fields: A dictionary mapping field names to the filter options available for that field.

    Filter Options:
        - 進捗: Range filter for '進捗' field.
        - TAT: Range filter for 'TAT' field.
        - 発生日: Date range filter for '発生日' field.
        - CLOSE日: Date range filter for 'CLOSE日' field.
        - 案件名: Case-insensitive filter for '案件名' field.
        - 機種名型番: Case-insensitive filter for '機種名型番' field.
        - 不良症状内容: Case-insensitive filter for '不良症状内容' field.
        - 責区: Exact match filter for '責区' field.
        - 責任者: Exact match filter for '責任者' field.
        - 発生場所: Exact match filter for '発生場所' field.
        - 製品分: Exact match filter for '製品分' field.
        - 分類: Exact match filter for '分類' field.
    """
    # 進捗 = django_filters.RangeFilter(field_name='進捗')
    # TAT = django_filters.RangeFilter(field_name='TAT')
    発生日 = django_filters.DateFromToRangeFilter(field_name='発生日', widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))
    # CLOSE日 = django_filters.DateFromToRangeFilter(field_name='CLOSE日', widget=DateRangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))
    案件名=django_filters.CharFilter(field_name='案件名', lookup_expr='icontains')
    機種名型番=django_filters.CharFilter(field_name='機種名型番', lookup_expr='icontains')
    不良症状内容=django_filters.CharFilter(field_name='不良症状内容', lookup_expr='icontains')

    class Meta:
        model = MajorQualityCase
        fields = {
            # 'id': ['exact'],
            # '市場発生': ['exact'],
            # '再発防止': ['exact'],
            # '出荷停止': ['exact'],
            '責区': ['exact'],
            '責任者': ['exact'],
            # 'TAT': [],
            '発生場所': ['exact'],
            '製品分': ['exact'],
            '分類' : ['exact'],
            # '案件名': ['icontains'],
            # '機種名型番': ['icontains'],
            # '進捗状況': ['icontains'],
            # '不良症状内容': ['icontains'],
            # '保留対象': [],
            # '依頼日': [],
            # '停止日': [],
            # '解除日': [],
            # '単品在庫': [],
            # '半製品在庫': [],
            # '完成品在庫': [],
            # '外部在庫': [],
            # '対応内容': [],
            # '実施予定日': [],
            # '実施実際日': [],
            # '実施部署': [],
            # '実施者': [],
            # '発生原因': [],
            # '流出原因': [],
            # 'なぜなぜ': [],
            # '分析完了予定日': [],
            # '分析完了実際日': [],
            # '是正処置発生対策': [],
            # '是正処置流出対策': [],
            # '是正処置再発防止': [],
            # '是正完了予定日': [],
            # '是正完了実際日': [],
            # 'CLOSE日': [],
        }