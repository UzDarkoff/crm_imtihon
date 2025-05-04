from drf_yasg.utils import swagger_auto_schema
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Student, Parents
from ..serializers import StudentSerializer, ParentsSerializer
from ..permissions import IsAdminOrStaff, IsTeacherOfGroup

# Studentni olish
class StudentListView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrStaff]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

# Yangi student yaratish
class StudentCreateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrStaff]

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Studentni olish, yangilash va o‘chirish
class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated,IsAdminOrStaff]

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentSerializer)
    def patch(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Parents modeli uchun ViewSet
class ParentsViewSet(ModelViewSet):
    queryset = Parents.objects.all()  # Barcha ota-onalarni olish uchun queryset
    serializer_class = ParentsSerializer  # ParentsSerializer ishlatiladi
    permission_classes = [IsAuthenticated,
                          IsAdminOrStaff]  # Faqat autentifikatsiyadan o‘tgan Admin yoki Staff uchun ruxsat