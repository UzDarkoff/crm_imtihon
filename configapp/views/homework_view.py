
from configapp.serializers.homework_serializer import  HomeworkSubmissionSerializer, \
    HomeworkCreateUpdateSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from ..serializers import HomeworkSerializer
from ..models import Homework



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StudentHomeworkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        homeworks = Homework.objects.filter(student=user)
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class TeacherHomeworkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkCreateUpdateSerializer
    @swagger_auto_schema(
        operation_description="O‘qituvchi o‘z guruhidagi vazifalarni ko‘rish",
        responses={200: HomeworkSerializer(many=True)},
        request_body=HomeworkCreateUpdateSerializer

    )
    def get_queryset(self):
        # O‘qituvchi o‘z guruhidagi vazifalarni ko‘rishi
        teacher = self.request.user.teacher_profile
        return Homework.objects.filter(created_by=teacher)

    @swagger_auto_schema(
        operation_description="O‘qituvchi yangi vazifa yaratishi",
        request_body=HomeworkCreateUpdateSerializer,
        responses={201: "Vazifa yaratildi"}
    )
    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(created_by=teacher)

    @swagger_auto_schema(
        operation_description="O‘qituvchi vazifani yangilashi",
        request_body=HomeworkCreateUpdateSerializer,
        responses={200: "Vazifa yangilandi"}
    )
    def perform_update(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(updated_by=teacher)
