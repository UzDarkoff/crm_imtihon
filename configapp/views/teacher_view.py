from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import Teacher
from ..serializers import TeacherSerializer
from ..permissions import IsAdminOrStaff, IsTeacherOfGroup
from rest_framework.permissions import IsAuthenticated


class TeacherListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        """
        Faqat admin yoki staff barcha teacherlarni ko‘rishi mumkin
        """
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def post(self, request):
        """
        Faqat admin yoki staff yangi teacher qo‘shishi mumkin
        """
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrStaff]

    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    def get(self, request, pk):
        teacher = self.get_object(pk)
        self.check_object_permissions(request, teacher)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def put(self, request, pk):
        teacher = self.get_object(pk)
        self.check_object_permissions(request, teacher)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = self.get_object(pk)
        self.check_object_permissions(request, teacher)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
