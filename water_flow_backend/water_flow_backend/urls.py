from apps.flow_rating.urls import *
from django.contrib import admin
from django.urls import path, include
from apps.user.urls import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('alert_water_consumption/', include('apps.alert_water_consumption.urls')),
    path('dialy_water_consumption/', include('apps.daily_water_consumption.urls')),
    path('weekly_water_consumption/', include('apps.weekly_water_consumption.urls')),
    path('monthly_water_consumption/', include('apps.monthly_water_consumption.urls')),
    path('bimonthly_water_consumption/', include('apps.bimonthly_water_consumption.urls')),
    ]
