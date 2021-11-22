from rest_framework import serializers
from .models import RecommendedArtifact

class RecommendedArtifactSerialize(serializers.ModelSerializer):
    class Meta:
        model = RecommendedArtifact
        fields = '__all__'
        # exclude = ('user',)