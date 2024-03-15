from django.contrib import admin
from .models import *

# @admin.register(plc)
# class plcAdmin(admin.ModelAdmin):
#     list_display = ["zone_a", "zone_b", "zone_c", "zone_d", "zone_e"]


# @admin.register(plcparameter)
# class plcparameterAdmin(admin.ModelAdmin):
#     list_display = ["Plc_make", "plc_series", "plc_ip", "plc_port", "plc_communication_type"]


# @admin.register(word_batch_read)
# class word_batch_readAdmin(admin.ModelAdmin):
#     list_display = ["startaddress", "readsize"]

# class ZoneDataInline(admin.TabularInline):
#     model = Zonedata
#     extra = 1

# @admin.register(LoadingStation)
# class LoadingStationAdmin(admin.ModelAdmin):
#     list_display = ["hanger_number", "live_status", "zone_number"]
#     inlines = [ZoneDataInline]



@admin.register(datalogger)
class dataloggerAdmin(admin.ModelAdmin):
    list_display = ["Plc_make", "plc_series", "plc_ip", "plc_port", "plc_communication_type"]

@admin.register(device_tag_setting)
class device_tag_settingAdmin(admin.ModelAdmin):
    list_display = ["plc", "address", "description", "data_type", "no_of_char"]

@admin.register(TriggerConfiguration)
class TriggerConfigurationAdmin(admin.ModelAdmin):
    list_display = ["tag", "trigger_enabled", "comment"]

@admin.register(datatrigger)
class datatriggerAdmin(admin.ModelAdmin):
    list_display = ["tag", "value", "timestamp"]	

@admin.register(datahistory)
class datahistoryAdmin(admin.ModelAdmin):
    list_display = ["count", "doublecount", "char", "date"]


