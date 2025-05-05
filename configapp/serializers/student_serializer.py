from .user_serializer import *
from ..models import Student, Parents


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        groups = validated_data.pop('group', [])  # groupni alohida ajratib olamiz

        user = UserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)

        student.group.set(groups)  # grouplarga set() orqali qo‘shamiz
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            UserSerializer().update(instance.user, user_data)

        for attr, value in validated_data.items():
            # ManyToManyField uchun alohida ishlov beramiz
            field = instance._meta.get_field(attr)
            if field.many_to_many:
                getattr(instance, attr).set(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance



# Parents modeli uchun serializer
class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents  # Qaysi model bilan ishlashini ko‘rsatadi
        # Seriyalizatsiya qilinadigan maydonlar
        fields = ['id', 'student', 'full_name', 'phone_number', 'address', 'descriptions']

