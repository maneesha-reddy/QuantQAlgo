from rest_framework import serializers
from .models import BackTest


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackTest
        fields = ("__all__")
