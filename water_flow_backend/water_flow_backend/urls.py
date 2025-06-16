# Django and Python Imports
from django.contrib import admin
from django.urls import path, include

# Project Imports
from core.utils.logs_view import * 
from core.authentication.views import *

# Defines the list of URL patterns for the entire project.
# Each 'path' function maps a URL route to a specific view.
urlpatterns = [

    # --- Admin Site ---
    # Provides access to the built-in Django admin interface.
    path('admin/', admin.site.urls),

    # --- Authentication Endpoints ---
    # Endpoint for users to submit their credentials (email/password) and receive an access/refresh token pair.
    path("token-auth/", TokenPairObtain.as_view(), name="token-auth"),
    # Endpoint for logging out, which should handle token invalidation on the server side.
    path('logout/', Logout.as_view(), name="logout"),
    # Endpoint to get a new access token using a valid refresh token.
    path('token-refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    
    # --- Application-Specific URLs ---
    # Includes all URL patterns defined within the 'alert_water_consumption' app.
    path('alert_water_consumption/', include('apps.alert_water_consumption.urls')),
    # Includes all URL patterns from the 'daily_water_consumption' app.
    path('daily_water_consumption/', include('apps.daily_water_consumption.urls')),
    # Includes all URL patterns from the 'weekly_water_consumption' app.
    path('weekly_water_consumption/', include('apps.weekly_water_consumption.urls')),
    # Includes all URL patterns from the 'monthly_water_consumption' app.
    path('monthly_water_consumption/', include('apps.monthly_water_consumption.urls')),
    # Includes all URL patterns from the 'bimonthly_water_consumption' app.
    path('bimonthly_water_consumption/', include('apps.bimonthly_water_consumption.urls')),

    # --- Log Viewing Endpoints ---
    # URL for viewing logs related to water consumption alerts.
    path('alert_logs/', LogsAlertWaterConsumption.as_view()),
    # URL for viewing logs related to daily water consumption. 
    # Note: There might be a typo in the view name 'LogsDialyWaterConsumption'. It could be 'LogsDailyWaterConsumption'.
    path('daily_logs/', LogsDialyWaterConsumption.as_view()),
    # URL for viewing logs related to weekly water consumption.
    path('weekly_logs/', LogsWeeklyWaterConsumption.as_view()),
    # URL for viewing logs related to monthly water consumption.
    path('monthly_logs/', LogsMonthlyWaterConsumption.as_view()),
    # URL for viewing logs related to bimonthly water consumption.
    path('bimonthly_logs/', LogsBimonthlyWaterConsumption.as_view())

]
