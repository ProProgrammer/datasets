import logging
import pickle
import zlib

import pandas as pd
from django.db import models

from core.models import AbstractTimeStampModel

logger = logging.getLogger(__name__)


class Dataset(AbstractTimeStampModel):
    """
    Django model encapsulates storage and methods on datasets uploaded using CSV

    # uuid inherited from TimeStampedModel acts as the primary key for objects of this model
    """

    file = models.FileField(blank=False, null=False)
    dataframe = models.BinaryField(editable=False, null=True, blank=True, default=None,
                                   help_text='Pandas DataFrame version of the file object')

    def __str__(self):
        return f'File: {self.file.name}'

    def save(self, *args, **kwargs):
        """
        Override default .save() (from `AbstractTimeStampModel` to auto populate BinaryField with output of file
        object in to a pandas dataframe.
        Try saving, however in case of exception move ahead for now, will handle exceptions as we go along. (
        Uncharted territory)
        """

        try:
            with self.file.open(mode='r+b') as file_object:
                pandas_dataframe = pd.read_csv(file_object)

            dataframe_as_bytes = pickle.dumps(pandas_dataframe)
            self.dataframe = zlib.compress(dataframe_as_bytes, level=9)
        except Exception as unhandled_exception:
            logger.error(
                f'Unhandled exception occurred, "{unhandled_exception}"'
            )
        finally:
            super(Dataset, self).save(*args, **kwargs)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Un-pickle the pandas dataframe if needed, else return as is.
        """

        return pickle.loads(zlib.decompress(self.dataframe))
