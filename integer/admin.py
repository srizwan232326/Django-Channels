from django.contrib import admin
from .models import *

@admin.register(plc)
class plcAdmin(admin.ModelAdmin):
    list_display = ["zone_a", "zone_b", "zone_c", "zone_d", "zone_e"]
