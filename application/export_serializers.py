from rest_framework import serializers
from .models import Application


class ExportApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        exclude = ['hacker', 'id']
