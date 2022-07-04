from rest_framework import serializers

from literatures_and_datum_management.models import DocumentSourceTable, LiteratureDataTable, UserLexicon


class DocumentSourceModelSerializer(serializers.ModelSerializer):
    """文献管理模型序列化器

    """
    class Meta:
        model = DocumentSourceTable
        fields = "__all__"


class LiteratureDataModelSerializer(serializers.ModelSerializer):
    """文献数据管理模型序列化器

    """
    class Meta:
        model = LiteratureDataTable
        fields = "__all__"


class UserLexiconModelSerializer(serializers.ModelSerializer):
    """用户词库管理序列化器

    """
    class Meta:
        model = UserLexicon
        fields = "__all__"
