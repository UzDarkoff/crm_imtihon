from rest_framework import serializers
from ..models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=False)  # ← is_staff default False qilib berish

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password', 'is_student', 'is_teacher', 'group', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_staff = validated_data.pop('is_staff', True)  # ← bu qo‘shilishi kerak
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_staff = is_staff  # ← bu alohida belgilanadi
        user.save()
        return user
