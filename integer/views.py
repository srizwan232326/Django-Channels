from django.shortcuts import render
from .models import plc
from channels.db import database_sync_to_async


def index(request):
    return render(request, 'index.html', context={'text': 'world'})

@database_sync_to_async
def save_plc_data_async(zone_a, zone_b, zone_c, zone_d, zone_e):
    plc_data = plc(zone_a=zone_a, zone_b=zone_b, zone_c=zone_c, zone_d=zone_d, zone_e=zone_e)
    plc_data.save()