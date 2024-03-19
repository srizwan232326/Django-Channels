from rest_framework import serializers
from .models import LoadingStation, Zonedata , datalogger , device_tag_setting , TriggerConfiguration , Triggerloggers

class LoadingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadingStation
        fields = ['hanger_number', 'live_status', 'zone_number']

class ZonedataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zonedata
        fields = ['loading_station', 'loading_zone_1', 'degrease_zone_2']



class DataloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = datalogger
        fields = '__all__'

class DeviceTagSettingSerializer(serializers.ModelSerializer):
    plc = DataloggerSerializer(required=False)

    class Meta:
        model = device_tag_setting
        fields = ['id', 'plc', 'address', 'description', 'data_type', 'no_of_char']



class TriggerConfigurationSerializer(serializers.ModelSerializer):
    tag = DeviceTagSettingSerializer()
    class Meta:
        model = TriggerConfiguration
        fields = '__all__'

class Triggerdataseralizer(serializers.ModelSerializer):
    triggertag = TriggerConfigurationSerializer()
    class Meta:
        model = Triggerloggers
        fields = '__all__'

class DataloggerSerializerfortag(serializers.ModelSerializer):
    class Meta:
        model = datalogger
        fields = ['plc_ip']  # Add other fields if needed

class DeviceTagSettingExtendedSerializer(serializers.ModelSerializer):
    plc = DataloggerSerializerfortag()

    class Meta:
        model = device_tag_setting
        fields = ['id', 'address', 'description', 'data_type', 'no_of_char', 'plc']
    
    def create(self, validated_data):
        plc_data = validated_data.pop('plc')
        datalogger_instance, created = datalogger.objects.get_or_create(**plc_data)
        validated_data['plc'] = datalogger_instance
        return super().create(validated_data)
    

class DeviceTagSettingSubsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = device_tag_setting
        fields = ['id', 'address', 'description', 'data_type', 'no_of_char']

class TriggerloggersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triggerloggers
        fields = '__all__'