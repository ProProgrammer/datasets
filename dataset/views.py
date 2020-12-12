from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from dataset.models import Dataset
from dataset.serializers import DatasetModelSerializer


class DatasetModelViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet allows for default functionality out of the box, see viewsets.ModelViewSet documentation
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetModelSerializer
    pagination_class = None

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to return only filename and size of the dataset object
        """

        dataset_object: Dataset = self.get_object()

        custom_response = {
            'file': dataset_object.file.name,
            'size': f'{dataset_object.file.size} bytes'
        }

        return Response(custom_response, status=HTTP_200_OK)
