from rest_framework import serializers
from .models import MajorQualityCase

class MajorQualityCaseSerializer(serializers.ModelSerializer):
    """
    Serializer for MajorQualityCase model to serialize/deserialize data.

    Attributes:
        責区: CharField - Responsible category name.
        責任者: CharField - Responsible user's username.
        製品分: CharField - Part category name.
        分類: CharField - Division category name.
        発生場所: CharField - Location name.
        実施部署: SerializerMethodField - Method to get handling department name.
        実施者: SerializerMethodField - Method to get handling user's username.

    Meta:
        model: MajorQualityCase - Model to be serialized/deserialized.
        fields: List[str] - List of fields to include in the serialized data.

    Methods:
        get_実施部署: Get handling department name for the object.
        get_実施者: Get handling user's username for the object.
    """
    責区 = serializers.SlugRelatedField(slug_field='name', read_only=True)
    責任者 = serializers.SlugRelatedField(slug_field='username', read_only=True)
    製品分 = serializers.SlugRelatedField(slug_field='name', read_only=True)
    分類 = serializers.SlugRelatedField(slug_field='name', read_only=True)
    発生場所 = serializers.SlugRelatedField(slug_field='name', read_only=True)
    実施部署 = serializers.SerializerMethodField()
    実施者 = serializers.SerializerMethodField()
    uuid = serializers.UUIDField(read_only=True)
    
    class Meta:
        depth = 1
        model = MajorQualityCase
        fields = [
            'uuid',
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

    def get_実施部署(self, obj: MajorQualityCase) -> (str | None):
        return obj.実施部署.name if obj.実施部署 else None

    def get_実施者(self, obj: MajorQualityCase) -> (str | None):
        return obj.実施者.username if obj.実施者 else None