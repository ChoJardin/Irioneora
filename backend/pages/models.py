from django.db import models


class RecommendedArtifact(models.Model):
    # desc,id_num,nationalityName,museumName,name
    id_num = models.CharField(max_length=100)
    image_uri = models.TextField()
    desc = models.TextField()
    museum_name = models.CharField(max_length=200, null=True, blank=True)
    nationality_name = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

 






