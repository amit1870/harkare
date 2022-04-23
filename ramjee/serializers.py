from rest_framework import serializers

from .models import Harkare

class HarkareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Harkare
        fields = ['name', 'url']