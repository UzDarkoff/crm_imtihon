from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    # Admin panelida foydalanuvchi maydonlari qanday ko‘rinishini belgilash
    ordering = ['id']

    # Ko‘rsatiladigan maydonlar ro‘yxati
    list_display = ['phone_number', 'email', 'is_active', 'is_admin', 'is_student', 'is_teacher']

    # Foydalanuvchi yaratishda ko‘rsatiladigan maydonlar
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),  # Telefon raqam va parol
        ('Personal Info', {'fields': ('email', 'username', 'group')}),  # Shaxsiy ma'lumotlar
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_admin', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),
        # Ruxsatnomalar
    )

    # Yangi foydalanuvchi qo‘shishda ko‘rsatiladigan maydonlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_student', 'is_teacher'),
        }),
    )

    # Qidiruv maydonlari
    search_fields = ['phone_number', 'email']

    # Filtrlash imkoniyatlari
    list_filter = ['is_active', 'is_teacher', 'is_student']


admin.site.register(
    [User, Course, Departments, GroupStudent, Teacher, Student, Attendance, Payment, Homework, Lesson, Table, TableType,
     Rooms, Day,Parents,])
