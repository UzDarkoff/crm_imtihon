from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from configapp.models import Student
from configapp.pagination import StandardResultsSetPagination
from configapp.permissions import IsAdminOrStaff


class StudentStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'start_date',
            openapi.IN_QUERY,
            description="Boshlanish sanasi (format: YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date'
        ),
        openapi.Parameter(
            'end_date',
            openapi.IN_QUERY,
            description="Tugash sanasi (format: YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date'
        )
    ])
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            students_in_range = Student.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
        else:
            students_in_range = Student.objects.all()

        ongoing_students_count = students_in_range.filter(status='ongoing').count()
        graduated_students_count = students_in_range.filter(status='graduated').count()
        total_students_count = students_in_range.count()

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(students_in_range, request)

        return paginator.get_paginated_response({
            'total': total_students_count,
            'ongoing': ongoing_students_count,
            'graduated': graduated_students_count,
            'students': [student.id for student in result_page]
        })
