from django.core import cache
from django_otp.plugins.otp_totp.models import TOTPDevice
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User
from ..serializers import SMSSerializer, VerifySMSSerializer



class OTPRequiredView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        device, created = TOTPDevice.objects.get_or_create(user=user, name="default")

        # OTP yuborish
        if not device.is_valid():
            device.generate_challenge()

        # OTP yuborilganini bildiruvchi javob
        return Response({"message": "OTP yuborildi"}, status=status.HTTP_200_OK)


class OTPVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        device = TOTPDevice.objects.get(user=user)

        # OTPni tekshirish
        otp_code = request.data.get('otp_code')  # foydalanuvchidan OTPni olish
        if device.verify_token(otp_code):
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


class VerifySms(APIView):
    pagination_class = PageNumberPagination

    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))
            if verification_code == str(cached_code):
                return Response({
                    'status': True,
                    'detail': 'OTP matched. please proceed for registration'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'otp INCOORECT'
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
