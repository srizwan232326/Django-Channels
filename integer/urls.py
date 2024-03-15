from django.urls import path
from integer import views
from integer.views import *

urlpatterns = [
    path('', views.test, name='test'),
    path('plc/', views.plc, name='plc'),
    path('api/dataloggers/', DataloggerListAPIView.as_view(), name='datalogger-list-api'),
    path('api/dataloggers/<int:pk>/', DataloggerDetailAPIView.as_view(), name='datalogger-detail'),

    
]

