from rest_framework import serializers
from .models import MonthlyWaterConsumption

class MonthlyWaterConsumptionSerializer(serializers.ModelSerializer):

    class Meta:

        model = MonthlyWaterConsumption
        fields = ['id', 'date_label', 'start_date', 'end_date', 'total_consumption']
