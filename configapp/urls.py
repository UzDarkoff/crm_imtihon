from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.attendance_view import GroupAttendanceView
from .views.group_view import DepartmentsViewSet, CourseViewSet, GroupStudentViewSet

from .views.login import *
from .views.register_view import RegisterUserApi
from .views.statistics_view import StudentStatisticsView
from .views.student_view import *

from .views.otp_view import OTPRequiredView, OTPVerifyView
from .views.payment_view import PaymentViewSet
from .views.teacher_view import TeacherListCreateView, TeacherDetailView
# urls.py
from rest_framework.routers import DefaultRouter
from .views import HomeworkListCreateApi, HomeworkSubmissionCreateApi

router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')
router.register(r'department', DepartmentsViewSet, 'department')
router.register(r'course', CourseViewSet, 'course')
router.register(r'group', GroupStudentViewSet, 'group')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUserApi.as_view(), name='register'),
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/create/', StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/statistics/', StudentStatisticsView.as_view(), name='student-statistics'),
    path('attendance/', GroupAttendanceView.as_view(), name='attendance'),
    path('homeworks/teacher-create', HomeworkListCreateApi.as_view(), name='homework-list-create'),
    path('homeworks/<int:homework_id>/submission/', HomeworkSubmissionCreateApi.as_view(),
         name='homework-submission-create'),
    path('otp/', OTPRequiredView.as_view(), name='otp_required'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += router.urls
