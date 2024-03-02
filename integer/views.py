from django.shortcuts import render
from .models import plc , plcparameter , LoadingStation, Zonedata
from channels.db import database_sync_to_async
import json
from django.db import transaction
from .tasks import print_test	

from django.shortcuts import render, HttpResponse
from realtime.celery import app
from celery.schedules import crontab
import pytz
from datetime import datetime

def index(request):
    return render(request, 'index.html', context={'text': 'world'})


@database_sync_to_async
def save_plc_data_async(hanger_no, live_status, zone_no, loading_intime, loading_outime):
    print("hanger_no", hanger_no, "live_status", live_status, "zone_no", zone_no, "loading_intime", loading_intime, "loading_outime", loading_outime)
    try:
        print("inside try")
        loading_station_instance = LoadingStation.objects.get(hanger_number=int(hanger_no), live_status=int(live_status))

        if int(zone_no) == 1:
            Zonedata.objects.create(
                loading_station=loading_station_instance,
                loading_zone1={"hello": "world"},
                
            )
        elif int(zone_no) == 2:
            Zonedata.objects.create(
                loading_station=loading_station_instance,
                degrease_zone2={"hello1": "world"},
            )


    except LoadingStation.DoesNotExist:
        print("LoadingStation does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")




def test(request):
    print_test.delay()
    return HttpResponse("Task has been created")