from django.contrib import admin
from django.urls import path
from integer.views import index , plc
from django.urls import include
from integer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('plc/', plc, name='plc'),
    path('api/', include('rest_framework.urls')),
    path('api/dataloggers/', DataloggerListAPIView.as_view(), name='datalogger-list-api'),
    path('api/dataloggers/<int:pk>/', DataloggerDetailAPIView.as_view(), name='datalogger-detail'),
    path('tag_master/', tag_master, name='tag_master'),
    path('dashboard/', dashboard, name='dashboard'),
    path('trigger/', trigger, name='trigger'),
    path('api/trigger-configurations/', TriggerSetting.as_view(), name='trigger-configurations-api'),
    path('api/trigger-setting/', TriggerSettingAPIView.as_view(), name='trigger-configurations-api'),
    path('api/trigger-setting/<int:config_id>/', TriggerSettingAPIView.as_view(), name='trigger_setting_detail'),
    path('api/device-tag-settings/', DeviceTagSettingListCreateView.as_view(), name='device-tag-settings-list-create'),
    path('api/device-tag-settings/<int:pk>/', DeviceTagSettingDetailView.as_view(), name='device-tag-settings-detail'),
    path('api/plc-ip-list/', PlcIpListView.as_view(), name='plc-ip-list'),




    
]
