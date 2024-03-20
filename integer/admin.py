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
    list_display = ["tag", "address", "comment"]

@admin.register(datatrigger)
class datatriggerAdmin(admin.ModelAdmin):
    list_display = ["tag", "value", "timestamp"]	

@admin.register(RobotCycleDataHistory)
class datahistoryAdmin(admin.ModelAdmin):
    list_display = ["daytime", "model", "color", "spare1", "spare2", "L_resin_Paint_cons", "L_hardener_Paint_cons", "L_ratio", "R_resin_Paint_cons", "R_hardener_Paint_cons", "R_ratio"]

@admin.register(LoadingstationData)
class LoadingstationDataAdmin(admin.ModelAdmin):
    list_display = ["created_at", "hanger_no", "program_no", "color_no", "color_code", "last_zone", "live_status", "category"]

@admin.register(part)
class partAdmin(admin.ModelAdmin):
    list_display = ["LoadingStation", "ln_code", "production_id", "quantity", "warehouse_id", "description"]

@admin.register(zonedata1)
class zonedata1Admin(admin.ModelAdmin):
    list_display = ["LoadingStation", "intime", "outtime", "pausetime"]

@admin.register(zonedata2)
class zonedata2Admin(admin.ModelAdmin):
    list_display = ["LoadingStation", "intime", "degrease_circ_pump", "degrease_heat_pump", "buner", "deg_hot_water_diff_prs", "deg_circ_pump_prs", "deg_circ_flow", "deg_tank_temp", "deg_tank_level"]
