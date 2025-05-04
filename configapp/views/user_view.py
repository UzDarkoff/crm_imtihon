from rest_framework import viewsets

from configapp.models import User
from configapp.serializers import UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        is_staff = self.request.data.get('is_staff', False)  # Swagger'dan is_staff olish
        serializer.save(is_staff=is_staff)  # User yaratishda is_staff ni saqlaymiz
