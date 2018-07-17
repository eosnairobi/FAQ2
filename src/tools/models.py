import uuid

from accounts.models import BlockProducer
from django.db import models


def tool_logo_directory_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/Tools/<ToolName>/<filename>
    return 'Tools/{0}/{1}'.format(instance.name, filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    creator_name = models.CharField(max_length=100)
    associated_bps = models.ManyToManyField(
        BlockProducer)
    categories = models.ManyToManyField('Category')
    description = models.CharField(max_length=1000)
    image = models.ImageField(blank=True, null=True,
                              upload_to=tool_logo_directory_path)
    url = models.URLField(blank=True, null=True)
    is_live = models.BooleanField(default=True)

    def __str(self):
        return self.name
