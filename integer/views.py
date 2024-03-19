from django.shortcuts import render
from .models import plc , plcparameter , LoadingStation, Zonedata , datalogger , device_tag_setting , datatrigger , datahistory , TriggerConfiguration , Triggerloggers
from channels.db import database_sync_to_async
import json
from django.shortcuts import render, HttpResponse
from realtime.celery import app
from celery.schedules import crontab
import pytz
from datetime import datetime 
from .serializers import DataloggerSerializer , DeviceTagSettingSerializer  , DeviceTagSettingExtendedSerializer , DeviceTagSettingSubsetSerializer , TriggerConfigurationSerializer , Triggerdataseralizer , TriggerloggersSerializer
from rest_framework import generics , renderers
from rest_framework import viewsets
from rest_framework import generics , renderers , status, views , viewsets 
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


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

def trigger_logger(request):
    return render(request, 'trigger_logger.html')

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
                'comment': config.comment
            }
            serialized_data.append(serialized_config)
        return JsonResponse({'trigger_configs': serialized_data})
    
    def post(self, request, *args, **kwargs):
        plc_make = request.POST.get('plcMake')
        plc_ip = request.POST.get('plcIp')
        tag_address = request.POST.get('tag')  
        comment = request.POST.get('comment')
        tags = device_tag_setting.objects.filter(plc__plc_ip=plc_ip, plc__Plc_make=plc_make)

        if not tags.exists():
            return JsonResponse({'message': 'Device tag setting not found'}, status=400)

        tag = tags.first()

        if TriggerConfiguration.objects.filter(tag=tag, address=tag_address).exists():
            return JsonResponse({'message': 'Trigger configuration with this address already exists'}, status=400)

        # Create and save the TriggerConfiguration
        trigger_config = TriggerConfiguration(tag=tag, address=tag_address, comment=comment)
        trigger_config.save()

        return JsonResponse({'message': 'Trigger details added successfully!'})
    
    def delete(self, request, *args, **kwargs):
        config_id = kwargs.get('config_id')
        address = kwargs.get('address')

        try:
            trigger_config = TriggerConfiguration.objects.get(tag__id=config_id, address=address)
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

class triggersettingapiview(generics.ListCreateAPIView):
    queryset = TriggerConfiguration.objects.all()
    serializer_class = TriggerConfigurationSerializer

class triggerdataapiview(generics.ListCreateAPIView):
    queryset = Triggerloggers.objects.all()
    serializer_class = Triggerdataseralizer

    def get(self, request, *args, **kwargs):
        trigger_loggers = Triggerloggers.objects.all()
        trigger_loggers_serializer = Triggerdataseralizer(trigger_loggers, many=True)
        response_data = {
            'trigger_loggers': trigger_loggers_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        trigger_address = request.data.get('triggertag')
        tag = request.data.get('tag')        
        trigger_configuration = TriggerConfiguration.objects.filter(address=trigger_address).first()  # Fetch TriggerConfiguration instance
        if trigger_configuration:
            trigger_logger = Triggerloggers.objects.create(
                triggertag=trigger_configuration,
                tag=tag
            )
            serializer = Triggerdataseralizer(trigger_logger)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Trigger Configuration not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        trigger_id = kwargs.get('pk')
        try:
            trigger_logger = Triggerloggers.objects.get(id=trigger_id)
            trigger_logger.delete()
            return Response({"message": "Trigger configuration deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Triggerloggers.DoesNotExist:
            return Response({"error": "Trigger configuration not found"}, status=status.HTTP_404_NOT_FOUND)