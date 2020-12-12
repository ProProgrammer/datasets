from rest_framework import viewsets

from dataset.models import Dataset
from dataset.serializers import DatasetModelSerializer


class DatasetModelViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet allows for default functionality out of the box, see viewsets.ModelViewSet documentation
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetModelSerializer
    pagination_class = None
