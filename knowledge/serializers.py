from rest_framework import serializers
from .models import KnowledgeGroup, Document, KBJob

class KnowledgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeGroup
        fields = ['id', 'name']

    def to_representation(self, instance):
        return {
            'knowledgeGroupId': instance.id,
            'knowledgeGroupName': instance.name
        }

class DocumentSubmitSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    knowledgeGroupId = serializers.CharField()

class KBSubmitSerializer(serializers.Serializer):
    links = serializers.CharField()
