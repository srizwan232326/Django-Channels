from django.contrib import admin
from django.urls import path
from integer.views import index
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    
]
