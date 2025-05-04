from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'id', 'phone_number', 'password', "email", 'is_active', 'is_admin', "is_staff", 'is_teacher', 'is_student')

