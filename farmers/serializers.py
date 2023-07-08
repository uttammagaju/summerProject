from rest_framework import serializers
from dashboard.models import Milk

class MilkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milk
        fields = ('fat', 'qty', 'rate', 'date', 'emp_id', 'farmer_id')