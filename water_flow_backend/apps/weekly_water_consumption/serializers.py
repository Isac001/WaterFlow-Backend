from rest_framework import serializers
from .models import WeeklyWaterConsumption

class WeeklyWaterConsumptionSerializer(serializers.ModelSerializer):

    class Meta:

        model = WeeklyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']