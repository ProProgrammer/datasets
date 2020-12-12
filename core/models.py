import uuid as uuid
from django.db import models
from django.utils import timezone


class AbstractTimeStampModel(models.Model):
    """
    Abstract base model that auto populates `created` and `modified` fields
    """

    # All models inheriting form AbstractTimeStampModel will have `uuid` field as their primary key
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    created = models.DateTimeField('Date created')
    modified = models.DateTimeField('Date updated')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override save method to update timestamps in created and modified fields
        Ref: https://stackoverflow.com/a/1737078/2661238
        """

        now = timezone.now()

        # Trigger the custom clean method if any
        self.full_clean()

        if not self.created:
            # If this is a new record, update the `created` date
            self.created = now

        # Finally, update the `modified` date, in case of a newly created record, this will be same as `created`
        self.modified = now

        super(AbstractTimeStampModel, self).save(*args, **kwargs)
