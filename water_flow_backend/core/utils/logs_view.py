from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.conf import settings

class LogsAlertWaterConsumption(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        log_alert = f"{settings.BASE_DIR}/core/logs_audit/alert_logs.txt"

        with open(log_alert, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=combined_logs.txt'

        return response
    
class LogsDialyWaterConsumption(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        log_alert = f"{settings.BASE_DIR}/core/logs_audit/daily_logs.txt"

        with open(log_alert, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=combined_logs.txt'

        return response
    
class LogsWeeklyWaterConsumption(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        log_alert = f"{settings.BASE_DIR}/core/logs_audit/weekly_logs.txt"

        with open(log_alert, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=combined_logs.txt'

        return response
    
class LogsMonthlyWaterConsumption(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        log_alert = f"{settings.BASE_DIR}/core/logs_audit/monthly_logs.txt"

        with open(log_alert, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=combined_logs.txt'

        return response
    
class LogsBimonthlyWaterConsumption(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):

        log_alert = f"{settings.BASE_DIR}/core/logs_audit/bimonthly_logs.txt"

        with open(log_alert, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=combined_logs.txt'

        return response