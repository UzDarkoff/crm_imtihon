from rest_framework.permissions import BasePermission


class IsAdminOrStaff(BasePermission):  # Faqat adminlar va stafflar uchun ruxsat beruvchi sinf
    def has_permission(self, request, view):  # Ruxsatni tekshirish metodi
        # Foydalanuvchi autentifikatsiyadan o'tgan va adminlik va stafflik ruxsati ruxsati bor:
        return request.user and request.user.is_authenticated and (request.user.is_admin or request.user.is_staff)

class IsTeacher(BasePermission): # Teacherlikka tekshirish
    def has_permission(self, request, view):
        # Foydalanuvchi autentifikatsiyadan o‘tganmi va u Teachermi:
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsStudent(BasePermission): # Studentlikka tekshirish
    def has_permission(self, request, view):
        # Foydalanuvchi autentifikatsiyadan o‘tganmi va u Studentmi:
        return request.user and request.user.is_authenticated and request.user.is_student

# Teacher uchun faqat o'z guruhlariga tegishli amallarni qilaolishi uchun permission
class IsTeacherOfGroup(BasePermission):
    def has_permission(self, request, view): #ruxsatni tekshiruvchi funksiya
        # Foydalanuvchi autentifikatsiyadan o‘tganmi va u Teachermi
        if not (request.user and request.user.is_authenticated and request.user.is_teacher):
            return False  # Agar Teacher bo‘lmasa, ruxsat berilmaydi

        # Tegishli guruh IDsini olish
        group_id = request.data.get('group') or request.query_params.get('group')
        if group_id: # Agar group_id kiritilgan bo'lsa
            # Teacherning guruhlari orasida shu ID li guruh borligini tekshiradi
            return request.user.teacher_profile.get_teacher.filter(id=group_id).exists()
        return True # agar guruh ID si kiritilmagan bo'lsa ruxsat beriladi(keyingi tekshirishga)

class IsAdminOrStaffOrStudentOrTeacher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated and (
                user.is_staff or
                getattr(user, 'is_student', False) or
                getattr(user, 'is_teacher', False)
            )
        )

from rest_framework.permissions import BasePermission

class IsTeacherOrStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated and (
                getattr(user, 'is_teacher', False) or
                getattr(user, 'is_student', False)
            )
        )
