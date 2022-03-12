
from rest_framework import serializers
from .models import customerInfo

class customerSerial(serializers.ModelSerializer):
    model = customerInfo
    fields = '__all__'