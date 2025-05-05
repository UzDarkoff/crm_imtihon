from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status as st
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from configapp.models import GroupStudent, User, Attendance
from configapp.permissions import IsAdminOrStaff, IsTeacher, IsStudent


class GroupAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff | IsTeacher|IsStudent]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('group_id', openapi.IN_QUERY, description="Guruh ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, description="Sana (format: YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: "OK"}
    )
    def get(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id')
        date = request.query_params.get('date')

        if not group_id or not date:
            return Response({"detail": "Group ID and Date are required."}, status=st.HTTP_400_BAD_REQUEST)

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format."}, status=st.HTTP_400_BAD_REQUEST)

        group = GroupStudent.objects.filter(id=group_id).first()
        if not group:
            return Response({"detail": "Group not found."}, status=st.HTTP_404_NOT_FOUND)

        students_in_group = group.students.filter(is_student=True)
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
                            'status': openapi.Schema(type=openapi.TYPE_STRING, description="Status: present, absent, or late")
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
            return Response({"detail": "Group ID, Date, and attendance data are required."}, status=st.HTTP_400_BAD_REQUEST)

        group = GroupStudent.objects.filter(id=group_id).first()
        if not group:
            return Response({"detail": "Group not found."}, status=st.HTTP_404_NOT_FOUND)

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format."}, status=st.HTTP_400_BAD_REQUEST)

        students_in_group = group.students.filter(is_student=True)

        for student in students_in_group:
            attendance = next((item for item in attendance_data if item.get('student_id') == student.id), None)
            if attendance:
                status = attendance.get('status')
                if status:
                    attendance_obj, created = Attendance.objects.get_or_create(student=student, group=group, date=date_obj)
                    attendance_obj.status = status
                    attendance_obj.save()
            else:
                attendance_obj, created = Attendance.objects.get_or_create(student=student, group=group, date=date_obj)
                attendance_obj.status = 'absent'
                attendance_obj.save()

        return Response({"detail": "Attendance updated successfully!"}, status=st.HTTP_200_OK)
