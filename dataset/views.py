import img2pdf
import numpy as np
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from dataset.helpers import export_to_excel
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


class DataActionViewSet(ViewSet):
    """
    Custom ViewSet that defines custom actions
    Ref: https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing

    This is being used to:
    - Export the dataset as an excel file
    - Return the stats generated by running df.describe() on the pandas dataframe as a json object
    - generate and return a PDF containing a list of histograms of all the numerical columns in the dataset
    """

    @action(detail=True)
    def excel(self, request, pk):
        """
        Export the dataset as an excel file
        """

        dataset_object: Dataset = get_object_or_404(queryset=Dataset.objects.all(), pk=pk)

        excel_file = export_to_excel(dataset_object)

        file_object = open(excel_file, 'r', encoding='ISO-8859-1')

        response = HttpResponse(file_object.readlines(),
                                content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename={excel_file}'

        return response

    @action(detail=True)
    def stats(self, request, pk):
        """
        Return the the stats generated by running df.describe() on the pandas dataframe as a json object
        """

        dataset_object: Dataset = get_object_or_404(queryset=Dataset.objects.all(), pk=pk)

        dataframe = dataset_object.get_dataframe()

        return Response(
            dataframe.describe().to_json(),
            status=HTTP_200_OK
        )

    @action(detail=True)
    def plot(self, request, pk):
        """
        Generate and return a PDF containing a list of histograms of all the numerical columns in the dataset
        """

        dataset_object: Dataset = get_object_or_404(queryset=Dataset.objects.all(), pk=pk)

        dataframe = dataset_object.get_dataframe()

        # Generate images
        for col in dataframe.select_dtypes(include=np.number):
            histogram = dataframe.hist(column=col)

            # Extract figure and store as JPEG file
            histogram[0][0].get_figure().savefig(f'{col}.jpeg')

        import glob
        current_timestamp = timezone.now()
        file_name_formatter = '%Y_%m_%d_%I_%M_%S_%p'

        file_name = f'{current_timestamp.strftime(file_name_formatter)}.pdf'

        with open(file_name, 'wb') as file_object:
            file_object.write(img2pdf.convert(glob.glob('./*.jpeg')))

        pdf_file = open(file_name, 'rb')
        return HttpResponse(pdf_file, content_type='application/pdf')
