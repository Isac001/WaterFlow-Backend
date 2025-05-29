# Import the admin module from Django's contrib package
from django.contrib import admin
# Import path and include functions for defining URL patterns
from django.urls import path, include
# Import all URL patterns from the user app (usually specific patterns are imported or router is used)
from apps.user.urls import * # This might import urlpatterns directly, or specific views/routers
# Import log views from the core.utils module
from core.utils.logs_view import * # Imports various log view classes
# Import TokenObtainPairView from rest_framework_simplejwt for JWT token generation
from rest_framework_simplejwt.views import TokenObtainPairView # Note: TokenRefreshView is used below but not imported here, assuming it's from simplejwt too.

# Define the list of URL patterns for the project
urlpatterns = [

    # Define the URL pattern for the Django admin site
    path('admin/', admin.site.urls),
    # Define the URL pattern for obtaining a JWT token pair (access and refresh tokens)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Define the URL pattern for refreshing an access token using a refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Assuming TokenRefreshView is from rest_framework_simplejwt.views
    # Include URL patterns from the alert_water_consumption app
    path('alert_water_consumption/', include('apps.alert_water_consumption.urls')),
    # Include URL patterns from the daily_water_consumption app
    path('daily_water_consumption/', include('apps.daily_water_consumption.urls')),
    # Include URL patterns from the weekly_water_consumption app
    path('weekly_water_consumption/', include('apps.weekly_water_consumption.urls')),
    # Include URL patterns from the monthly_water_consumption app
    path('monthly_water_consumption/', include('apps.monthly_water_consumption.urls')),
    # Include URL patterns from the bimonthly_water_consumption app
    path('bimonthly_water_consumption/', include('apps.bimonthly_water_consumption.urls')),
    # Define the URL pattern for viewing alert water consumption logs (Typo: loga_alert -> logs_alert?)
    path('loga_alert/', LogsAlertWaterConsumption.as_view()),
    # Define the URL pattern for viewing daily water consumption logs (Typo: dialy_logs -> daily_logs?)
    path('dialy_logs/', LogsDialyWaterConsumption.as_view()),
    # Define the URL pattern for viewing weekly water consumption logs
    path('weekly_logs/', LogsWeeklyWaterConsumption.as_view()),
    # Define the URL pattern for viewing monthly water consumption logs
    path('monthly_logs/', LogsMonthlyWaterConsumption.as_view()),
    # Define the URL pattern for viewing bimonthly water consumption logs (Note: trailing slash is missing, unlike others)
    path('bimonthly_logs', LogsBimonthlyWaterConsumption.as_view())

]