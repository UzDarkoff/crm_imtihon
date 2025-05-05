from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..serializers import *
from ..permissions import *

# departments uchun
class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()  # Barcha departmentsni olish
    serializer_class = DepartmentSerializer  # departments uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Course uchun
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()  # Barcha Courseni olish
    serializer_class = CourseSerializer  # Course uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar



class TeacherGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupStudentSerializer

    @swagger_auto_schema(
        operation_description="O‘qituvchi o‘z guruhlarini ko‘rishi",
        responses={200: GroupStudentSerializer(many=True)}
    )
    def get_queryset(self):
        # O‘qituvchi o‘z guruhlarini ko‘rishi
        teacher = self.request.user.teacher_profile
        return GroupStudent.objects.filter(teacher__in=[teacher])

    def perform_create(self, serializer):
        # Guruh yaratish faqat admin yoki staff uchun bo‘lishi kerak
        if not self.request.user.is_staff:
            raise PermissionDenied("Siz guruh yaratishga ruxsatga ega emassiz.")
        # Guruhni yaratishda admin yoki staffni tekshirish
        serializer.save(teacher=None)  # Teacher ni faqat admin yoki staff qo‘shishi mumkin


class StudentGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupStudentSerializer

    @swagger_auto_schema(
        operation_description="O‘quvchi o‘z guruhlarini ko‘rishi",
        responses={200: GroupStudentSerializer(many=True)}
    )
    def get_queryset(self):
        # O‘quvchi faqat o‘z guruhlarini ko‘rishi
        student = self.request.user.student_profile
        return GroupStudent.objects.filter(id__in=[group.id for group in student.group.all()])

    def perform_create(self, serializer):
        # Bu yerni admin yoki staff guruh yaratish ruxsatiga qo‘ymoqchi bo‘lsak, quyidagi qadamlarni kiritamiz:
        if not self.request.user.is_staff:
            raise PermissionDenied("Siz guruh yaratishga ruxsatga ega emassiz.")
        serializer.save(student=None)  # Admin yoki staff guruh yaratadi

# Day uchun
class DayViewSet(ModelViewSet):
    queryset = Day.objects.all()  # Barcha Dayni olish
    serializer_class = DaySerializer  # Day uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Rooms uchun
class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()  # Barcha Roomsni olish
    serializer_class = RoomsSerializer  # Rooms uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar



# TableType uchun
class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()  # Barcha TableTypeni olish
    serializer_class = TableTypeSerializer  # TableType uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Table uchun
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()  # Barcha Tableni olish
    serializer_class = TableSerializer  # Table uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar




class GroupStudentViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.all()
    serializer_class = GroupStudentSerializer
    permission_classes = [IsAuthenticated]  # Foydalanuvchi autentifikatsiya qilishi kerak

    @swagger_auto_schema(
        operation_description="Guruhni yaratish (Admin yoki Staff uchun)",
        request_body=GroupStudentSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Guruhlarni ko‘rish",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Guruhni yangilash",
        request_body=GroupStudentSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Guruhni qisman yangilash",
        request_body=GroupStudentSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Guruhni o‘chirish",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

