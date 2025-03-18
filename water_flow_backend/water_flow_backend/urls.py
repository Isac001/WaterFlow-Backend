from reader_leak.urls import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reader_leak.urls')),
]
