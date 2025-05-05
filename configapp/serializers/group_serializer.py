from rest_framework import serializers  # DRF serializerlarini yaratish uchun modul
from ..models import *  # Serializer uchun kerak bo'lgan modullar

# Day modeli uchun serializer
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day  # Model nomi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# Rooms modeli uchun serializer
class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms  # Model nomi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# TableType modeli uchun serializer
class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType  # Model nomi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# Table modeli uchun serializer
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table  # Model nomi
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']

# GroupStudent modeli uchun serializer
from rest_framework import serializers


class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'title', 'course', 'teacher', 'table', 'start_date', 'end_date', 'descriptions']
