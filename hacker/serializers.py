from rest_framework import serializers
from .models import Hacker


class ListHackersSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.user.get_full_name')
    state = serializers.CharField(source='profile.state')

    class Meta:
        model = Hacker
        fields = ['id', 'name', 'state']
