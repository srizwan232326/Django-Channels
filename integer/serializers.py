from rest_framework import serializers
from .models import LoadingStation, Zonedata

class LoadingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadingStation
        fields = ['hanger_number', 'live_status', 'zone_number']

class ZonedataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zonedata
        fields = ['loading_station', 'loading_zone_1', 'degrease_zone_2']
