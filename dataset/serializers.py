from rest_framework import serializers

from dataset.models import Dataset


class DatasetModelSerializer(serializers.ModelSerializer):
    """
    Base model serializer for DatasetModelViewSet
    """

    class Meta:
        model = Dataset
        fields = '__all__'
