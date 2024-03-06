from django.shortcuts import render
from .models import plc , plcparameter , LoadingStation, Zonedata , datalogger , device_tag_setting , datatrigger , datahistory
from channels.db import database_sync_to_async
import json
from django.shortcuts import render, HttpResponse
from realtime.celery import app
from celery.schedules import crontab
import pytz
from datetime import datetime

def index(request):
    return render(request, 'index.html', context={'text': 'world'})


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

