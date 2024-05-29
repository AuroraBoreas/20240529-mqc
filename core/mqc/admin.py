from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    MajorQualityCase,
    PartCategory,
    Department,
    Location,
    ResponsibilityCategory
)

admin.site.register(PartCategory)
admin.site.register(Department)
admin.site.register(ResponsibilityCategory)
admin.site.register(Location)

@admin.register(MajorQualityCase)
class MajorQualityCaseImportExportAdmin(ImportExportModelAdmin):
    list_display = [
            'id',
            '責区',
            '責任者',
            '製品分',
            '分類',
            '案件名',
            '機種名型番',
            '発生場所',
            '発生日',
            'CLOSE日',
    ]
    # list_filter = [
    #     '責任者',
    # ]

class MajorQualityCaseResource(resources.ModelResource):
    class Meta:
        model = MajorQualityCase
        fields = (
            'uuid',
            '進捗',
            '市場発生',
            '再発防止',
            '出荷停止',
            '責区__name',
            '責任者__username',
            'TAT',
            '製品分__name',
            '分類__name',
            '案件名',
            '機種名型番',
            '進捗状況',
            '発生場所__name',
            '発生日',
            '不良症状内容',
            '保留対象',
            '依頼日',
            '停止日',
            '解除日',
            '単品在庫',
            '半製品在庫',
            '完成品在庫',
            '外部在庫',
            '対応内容',
            '実施予定日',
            '実施実際日',
            '実施部署__name',
            '実施者__username',
            '発生原因',
            '流出原因',
            'なぜなぜ',
            '分析完了予定日',
            '分析完了実際日',
            '是正処置発生対策',
            '是正処置流出対策',
            '是正処置再発防止',
            '是正完了予定日',
            '是正完了実際日',
            'CLOSE日',
        )
        # export_order = (
        #     '進捗',
        #     '発生日',
        #     '案件名',
        #     '発生場所',
        #     '不良症状内容',
        #     '責任者__username',
        # )