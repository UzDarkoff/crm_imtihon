from rest_framework import serializers
from ..models import Payment

# Payment modeli uchun serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment  # Model nomi
        fields = ['id', 'student', 'amount', 'date', 'status'] # Seriyalizatsiya qilinadigan maydonlar
