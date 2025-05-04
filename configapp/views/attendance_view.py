from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime
from ..models import Attendance, GroupStudent, User

from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminOrStaff, IsTeacherOfGroup, IsTeacher


class GroupAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff | IsTeacher]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'group_id', openapi.IN_QUERY,
                description="Guruh ID",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'date', openapi.IN_QUERY,
                description="Sana (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={200: "OK"}
    )
    def get(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id')
        date = request.query_params.get('date')

        # Group ID va Date parametrlari tekshiriladi
        if not group_id or not date:
            return Response({"detail": "Group ID and Date are required."}, status=st.HTTP_400_BAD_REQUEST)

        # Sana formatini tekshirish
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format."}, status=st.HTTP_400_BAD_REQUEST)

        # Guruhni topish
        group = GroupStudent.objects.filter(id=group_id).first()
        if not group:
            return Response({"detail": "Group not found."}, status=st.HTTP_404_NOT_FOUND)

        # Guruhdagi talabalarning davomatlarini olish
        students_in_group = User.objects.filter(groupstudent__group=group)

        # Davomatlarni ro'yxatga olish
        attendance_list = []
        for student in students_in_group:
            attendance = Attendance.objects.filter(student=student, group=group, date=date_obj).first()
            if not attendance:
                attendance = Attendance(student=student, group=group, date=date_obj, status='absent')
                attendance.save()

            attendance_list.append({
                'student_id': student.id,
                'student_name': student.phone_number,
                'status': attendance.status
            })

        return Response({"attendance_data": attendance_list}, status=st.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'group_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Guruh ID"),
                'date': openapi.Schema(type=openapi.TYPE_STRING, description="Sana (YYYY-MM-DD format)"),
                'attendance_data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'student_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Talaba ID"),
                            'status': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description="Status: present, absent, or late")
                        }
                    ),
                    description="Davomat ma'lumotlari"
                )
            }
        ),
        responses={200: "OK"}
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        group_id = data.get('group_id')
        date = data.get('date')
        attendance_data = data.get('attendance_data')

        if not group_id or not date or not attendance_data:
            return Response({"detail": "Group ID, Date, and attendance data are required."},
                            status=st.HTTP_400_BAD_REQUEST)

        # Guruhni topamiz
        group = GroupStudent.objects.filter(id=group_id).first()
        if not group:
            return Response({"detail": "Group not found."}, status=st.HTTP_404_NOT_FOUND)

        # Sana formatini tekshiramiz
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format."}, status=st.HTTP_400_BAD_REQUEST)

        # Guruhdagi barcha talabalarni tekshiramiz
        students_in_group = User.objects.filter(groupstudent__group=group)

        # Har bir o'quvchining davomatini yangilaymiz
        for student in students_in_group:
            # Kelgan talabalarni tekshiramiz
            attendance = next((item for item in attendance_data if item.get('student_id') == student.id), None)

            # Agar student kelgan bo'lsa, statusni yangilaymiz
            if attendance:
                status = attendance.get('status')
                if status:
                    attendance_obj, created = Attendance.objects.get_or_create(student=student, group=group,
                                                                               date=date_obj)
                    attendance_obj.status = status
                    attendance_obj.save()
            else:
                # Agar student kelmagan bo'lsa, statusini absent qilib saqlaymiz
                attendance_obj, created = Attendance.objects.get_or_create(student=student, group=group, date=date_obj)
                attendance_obj.status = 'absent'
                attendance_obj.save()

        return Response({"detail": "Attendance updated successfully!"}, status=st.HTTP_200_OK)
