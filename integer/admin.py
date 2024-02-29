from django.contrib import admin
from .models import *

@admin.register(plc)
class plcAdmin(admin.ModelAdmin):
    list_display = ["zone_a", "zone_b", "zone_c", "zone_d", "zone_e"]


@admin.register(plcparameter)
class plcparameterAdmin(admin.ModelAdmin):
    list_display = ["Plc_make", "plc_series", "plc_ip", "plc_port", "plc_communication_type"]


@admin.register(word_batch_read)
class word_batch_readAdmin(admin.ModelAdmin):
    list_display = ["startaddress", "readsize"]