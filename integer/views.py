from django.shortcuts import render
from .models import plc , plcparameter , LoadingStation, Zonedata , datalogger , device_tag_setting , datatrigger , datahistory , TriggerConfiguration
from channels.db import database_sync_to_async
import json
from django.shortcuts import render, HttpResponse
from realtime.celery import app
from celery.schedules import crontab
import pytz
from datetime import datetime 
from .serializers import DataloggerSerializer , DeviceTagSettingSerializer  , DeviceTagSettingExtendedSerializer , DeviceTagSettingSubsetSerializer
from rest_framework import generics , renderers
from rest_framework import viewsets
from rest_framework import generics
from django.http import JsonResponse
from django.views import View



def index(request):
    return render(request, 'index.html', context={'text': 'world'})

def dashboard(request):
    return render(request, 'dashboard.html')

def plc(request):
    return render(request, 'plc.html')

def trigger(request):
    return render(request, 'trigger.html')

def tag_master(request):
    return render(request, 'tag_master.html')

@database_sync_to_async
def save_plc_data_async(*args):
    try:
        datahistory.objects.create(
            count=args[0],
            doublecount=args[1],
            char=args[2],
        )
    except device_tag_setting.DoesNotExist:
        print("device_tag_setting does not exist for address:")
    except Exception as e:
        print(f"An error occurred: {e}")

@database_sync_to_async
def save_trigger_data_async(tag, value):
    try:
        print("tag:", tag , "value:", value)
        device_tag = device_tag_setting.objects.get(address=tag)        
        datatrigger.objects.create(
            tag=device_tag,
            value=value
        )
    except device_tag_setting.DoesNotExist:
        print("device_tag_setting does not exist for tag:", tag)
    except Exception as e:
        print(f"An error occurred: {e}")





#///////////////////////////////////////FOR FROTEND//////////////////////////////////////////
class DataloggerListAPIView(generics.ListCreateAPIView):
    queryset = datalogger.objects.all()
    serializer_class = DataloggerSerializer
    renderer_classes = [renderers.JSONRenderer]

class DataloggerDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = datalogger.objects.all()
    serializer_class = DataloggerSerializer
    renderer_classes = [renderers.JSONRenderer]


class TriggerSetting(generics.ListCreateAPIView):
    queryset = device_tag_setting.objects.all()
    serializer_class = DeviceTagSettingSerializer
    renderer_classes = [renderers.JSONRenderer]



from django.http import JsonResponse
from django.views import View
from .models import TriggerConfiguration, device_tag_setting

class TriggerSettingAPIView(View):
    def get(self, request, *args, **kwargs):
        trigger_configs = TriggerConfiguration.objects.all()

        if not trigger_configs.exists():
            return JsonResponse({'message': 'No trigger configurations found'}, status=404)

        serialized_data = []
        for config in trigger_configs:
            serialized_config = {
                'tag_id': config.tag.id,
                'plc_ip': config.tag.plc.plc_ip,
                'plc_make': config.tag.plc.Plc_make,
                'address': config.address,
                'trigger_enabled': config.trigger_enabled,
                'comment': config.comment
            }
            serialized_data.append(serialized_config)
        return JsonResponse({'trigger_configs': serialized_data})
    
    def post(self, request, *args, **kwargs):
        plc_make = request.POST.get('plcMake')
        plc_ip = request.POST.get('plcIp')
        tag_address = request.POST.get('tag')  # Assuming 'tag' is the address of the device_tag_setting record
        trigger_enabled = request.POST.get('triggerEnabled')
        comment = request.POST.get('comment')
        tags = device_tag_setting.objects.filter(plc__plc_ip=plc_ip , plc__Plc_make=plc_make)

        if not tags.exists():
            return JsonResponse({'message': 'Device tag setting not found'}, status=400)
        tag = tags.first()

        trigger_config = TriggerConfiguration(
            tag=tag,
            address=tag_address,
            trigger_enabled=trigger_enabled,
            comment=comment
        )
        trigger_config.save()

        return JsonResponse({'message': 'Trigger details added successfully!'})
    
    def delete(self, request, *args, **kwargs):
        config_id = kwargs.get('config_id')

        try:
            trigger_config = TriggerConfiguration.objects.get(id=config_id)
            trigger_config.delete()
            return JsonResponse({'message': 'Trigger configuration deleted successfully!'})
        except TriggerConfiguration.DoesNotExist:
            return JsonResponse({'message': 'Trigger configuration not found'}, status=404)




class DeviceTagSettingListCreateView(generics.ListCreateAPIView):
    queryset = device_tag_setting.objects.all()
    serializer_class = DeviceTagSettingExtendedSerializer  # Use Extended Serializer for listing

class DeviceTagSettingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = device_tag_setting.objects.all()
    serializer_class = DeviceTagSettingSubsetSerializer  # Use Subset Serializer f


class PlcIpListView(View):
    def get(self, request, *args, **kwargs):
        plc_ips = datalogger.objects.values_list('plc_ip', flat=True).distinct()
        return JsonResponse(list(plc_ips), safe=False)