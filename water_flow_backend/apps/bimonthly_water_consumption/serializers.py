# Django and project imports
from rest_framework import serializers
from .models import BimonthlyWaterConsumption

# Serializer Class
class BimonthlyWaterConsumptionSerializer(serializers.ModelSerializer):

    # Class Meta to define model and fields
    class Meta:

        model = BimonthlyWaterConsumption
        fields = ['id','date_label', 'start_date', 'end_date', 'total_consumption']