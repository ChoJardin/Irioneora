from django.db import models
from django.conf import settings


# Create your models here.
class Artifact(models.Model):
    identification_number = models.CharField(max_length=100)
    image_uri = models.TextField()
    artifact_name = models.TextField(null=True, blank=True)


class ArtifactDetail(models.Model):
    identification_number = models.CharField(max_length=100)
    artifact_name = models.CharField(max_length=100)
    artifact_size = models.CharField(max_length=100, blank=True)
    artifact_author = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    museum_name = models.CharField(max_length=20, blank=True)
    index_words = models.TextField(blank=True)
    nationality_name = models.CharField(max_length=50, blank=True)
    image_uri = models.TextField()