from django.db import models

from core.models import AbstractTimeStampModel


class Dataset(AbstractTimeStampModel):
    """
    Django model encapsulates storage and methods on datasets uploaded using CSV

    # uuid inherited from TimeStampedModel acts as the primary key for objects of this model
    """

    file = models.FileField(blank=False, null=False)
