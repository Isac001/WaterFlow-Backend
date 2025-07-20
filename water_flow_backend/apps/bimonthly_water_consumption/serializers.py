# Django and project imports
from rest_framework import serializers
from .models import BimonthlyWaterConsumption
from apps.monthly_water_consumption.models import MonthlyWaterConsumption

# Serializer Class
class BimonthlyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Class Meta to define model and fields
    class Meta:

        model = BimonthlyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']

class MonthsOnBimonthlySerializer(serializers.ModelSerializer):

    consumption = serializers.DecimalField(
        source = 'total_consumption',
        max_digits=20,
        decimal_places=2
    )

    class Meta:

        model = MonthlyWaterConsumption

        fields = ['start_date', 'end_date', 'consumption']