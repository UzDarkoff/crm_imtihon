from .user_serializer import *
from ..models import Departments, Course, Teacher


class DepartmentSerializer(serializers.ModelSerializer):# Department uchun Serializers:
    class Meta:
        model = Departments # Model nomi
        fields = ['id', 'title', 'is_active', 'descriptions'] #Serializatsiya qilinadigan maydonlar

class CourseSerializer(serializers.ModelSerializer): # Course uchun Serialzier
    class Meta:
        model = Course  # Model nomi
        fields = ['id', 'title', 'descriptions']# Seriyalizatsiya qilinadigan maydonlar



class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    departments = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(), many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        departments = validated_data.pop('departments', [])
        courses = validated_data.pop('course', [])
        user = UserSerializer().create(user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.departments.set(departments)
        teacher.course.set(courses)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        departments = validated_data.pop('departments', None)
        courses = validated_data.pop('course', None)

        if user_data:
            UserSerializer().update(instance.user, user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if departments is not None:
            instance.departments.set(departments)
        if courses is not None:
            instance.course.set(courses)
        return instance
