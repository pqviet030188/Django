from rest_framework import serializers
from .models import Bill
from .models import Instalment
from .models import BillImage

class BillImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillImage
        fields = ['id', 'image']

class BillSerializer(serializers.ModelSerializer):
    images = BillImageSerializer(many=True, read_only=True)  # Use related_name here

    class Meta:
        model = Bill
        fields = ['id', 'biller', 'amount', 
                  'date', 'status', 'status_context', 'images']

class InstalmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instalment
        fields = ['id', 'bill_id', 'amount', 'due', 'status']