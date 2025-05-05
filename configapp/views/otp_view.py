from django.contrib.auth import update_session_auth_hash
from django.core import cache
from django_otp.plugins.otp_totp.models import TOTPDevice
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from ..serializers import SMSSerializer, VerifySMSSerializer, ChangePasswordSerializer

import pyotp
from django_otp.plugins.otp_totp.models import TOTPDevice

import pyotp
from django_otp.plugins.otp_totp.models import TOTPDevice

import random
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache


class OTPRequiredView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request):
        user = request.user

        # 4 xonali tasodifiy OTP yaratish
        otp_code = random.randint(1000, 9999)

        # OTPni 5 daqiqa davomida keshga saqlash
        cache.set(f"otp_{user.id}", otp_code, timeout=300)

        return Response({
            "message": "OTP yuborildi",
            "otp": otp_code
        }, status=status.HTTP_200_OK)


def send_sms(phone_number, otp_code):
    # Bu yerda SMS yuborish jarayoni amalga oshirilishi kerak
    print(f"OTP: {otp_code} yuborildi telefon raqamiga: {phone_number}")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class OTPVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        user = request.user
        otp_code = request.data.get('otp_code')  # foydalanuvchidan OTPni olish

        # Foydalanuvchining OTP kodini keshdan olish
        cached_otp = cache.get(f"otp_{user.id}")

        if cached_otp is None:
            return Response({"message": "OTP muddati o'tgan yoki yuborilmagan"}, status=status.HTTP_400_BAD_REQUEST)

        # OTPni tekshirish
        if str(cached_otp) == str(otp_code):
            return Response({"message": "OTP tasdiqlandi"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "OTP xato"}, status=status.HTTP_400_BAD_REQUEST)


class PhoneSendOTP(APIView):
    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        print(phone_number)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone_number__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'phone number already exist'
                })
            else:
                key = send_otp(phone)

                if key:
                    # Store the verification code and phone number in cache for 5 minutes
                    cache.set(phone_number, key, 600)

                    return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)

                return Response({"message": "Failed to send SMS"}, status=status.HTTP_400_BAD_REQUEST)

import random
def send_otp(phone):
    if phone:
        key = random.randint(1001,9999)
        print(key)
        return key
    else:
        return False

# views.py
class VerifySms(APIView):
    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))

            if verification_code == cached_code:
                # OTP tasdiqlandi, endi parolni o‘zgartirishni amalga oshiramiz
                new_password = request.data.get('new_password')
                if new_password:
                    user = User.objects.filter(phone_number=phone_number).first()
                    if user:
                        user.set_password(new_password)
                        user.save()
                        return Response({
                            'status': True,
                            'detail': 'Parol muvaffaqiyatli yangilandi.'
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({'status': False, 'detail': 'Foydalanuvchi topilmadi.'})
                return Response({'status': False, 'detail': 'Yangi parol kiritilmadi.'})

            return Response({
                'status': False,
                'detail': 'OTP noto‘g‘ri'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            # Foydalanuvchining parolini yangilash
            user.set_password(new_password)
            user.save()

            return Response({"message": "Parol muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
