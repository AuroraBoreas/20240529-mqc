from django import forms
from .models import (
    MajorQualityCase,
    PartCategory,
    Department,
    ResponsibilityCategory
)

class PartCategoryForm(forms.ModelForm):
    class Meta:
        model = PartCategory
        fields = ['name',]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name',]

class ResponsibilityCategoryForm(forms.ModelForm):
    class Meta:
        model = ResponsibilityCategory
        fields = ['name',]

class DateInputWidget(forms.DateInput):
    input_type = 'date'

class MajorQualityCaseForm(forms.ModelForm):
    """
    A form class for creating and updating instances of MajorQualityCase model.

    Attributes:
        model (MajorQualityCase): The model class for which the form is created.
        fields (str): A string indicating all fields of the model to be included in the form.
        widgets (dict): A dictionary mapping field names to custom widget instances for rendering in the form.

    Widget Customizations:
        - '発生日': DateInputWidget()
        - '依頼日': DateInputWidget()
        - '停止日': DateInputWidget()
        - '解除日': DateInputWidget()
        - '実施予定日': DateInputWidget()
        - '実施実際日': DateInputWidget()
        - '分析完了予定日': DateInputWidget()
        - '分析完了実際日': DateInputWidget()
        - '是正完了予定日': DateInputWidget()
        - '是正完了実際日': DateInputWidget()
        - 'CLOSE日': DateInputWidget()
        - '進捗': forms.TextInput(attrs={'placeholder': '0-100'})
    """
    class Meta:
        model = MajorQualityCase
        fields = [
            '進捗',
            '市場発生',
            '再発防止',
            '出荷停止',
            '責区',
            '責任者',
            'TAT',
            '製品分',
            '分類',
            '案件名',
            '機種名型番',
            '進捗状況',
            '発生場所',
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
            '実施部署',
            '実施者',
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
        ]
        widgets = {
            '発生日': DateInputWidget(), 
            '依頼日': DateInputWidget(),
            '停止日': DateInputWidget(),
            '解除日': DateInputWidget(),
            '実施予定日': DateInputWidget(),
            '実施実際日': DateInputWidget(),
            '分析完了予定日': DateInputWidget(),
            '分析完了実際日': DateInputWidget(),
            '是正完了予定日': DateInputWidget(),
            '是正完了実際日': DateInputWidget(),
            'CLOSE日': DateInputWidget(),
            '進捗': forms.TextInput(attrs={'placeholder': '0-100'}),
        }

class MajorQualityCaseDownloadFormatForm(forms.Form):
    FormatChoices = [
        ('csv', 'csv'),
        ('json', 'json'),
    ]
    format = forms.ChoiceField(
        choices=FormatChoices,
        widget=forms.Select(attrs={'class':'form-select'})
    )
