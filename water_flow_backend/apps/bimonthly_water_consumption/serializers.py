from rest_framework import serializers
from .models import BimonthlyWaterConsumption

class BimonthlyWaterConsumptionSerializer(serializers.ModelSerializer):

    class Meta:

        model = BimonthlyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']