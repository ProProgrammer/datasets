from django.utils import timezone

from dataset.models import Dataset


def export_to_excel(dataset: Dataset) -> str:
    """
    Given a Dataset object, export its `file` in excel and return the file name

    Return: file_name with extension in str format
    """

    dataframe = dataset.get_dataframe()

    current_timestamp = timezone.now()
    file_name_formatter = '%Y_%m_%d_%I_%M_%S_%p'

    file_name = f'{current_timestamp.strftime(file_name_formatter)}.xls'

    # generate excel file
    dataframe.to_excel(file_name)

    return file_name
