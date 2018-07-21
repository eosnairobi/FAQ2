from django.db import models


class CommunitySuggestedTool(models.Model):
    pass


class GeneralSuggestion(models.Model):
    author = models.CharField(max_length=50, null=True)
    topic = models.CharField(max_length=50, null=True)
    content = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.topic


