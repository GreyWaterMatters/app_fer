from django.db import models


class Document(models.Model):
    class Meta:
        app_label = 'web_ai'
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()