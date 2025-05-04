from .user_serializer import *

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'group', 'is_line', 'descriptions']

    def create(self, validated_data):  # yangi student yaratish
        user_data = validated_data.pop('user')  # user ma'lumotlarini ajratib olish
        group_data = validated_data.pop('group')  # groupni alohida ajratib olamiz
        user = User.objects.create_user(**user_data)  # user ma'lumotlari asosida yangi user yaratish
        student = Student.objects.create(user=user, **validated_data)  # student yaratish
        student.group.set(group_data)  # M2M uchun .set() ishlatamiz
        return student

    def update(self, instance, validated_data):  # student ma'lumotlarini tahrirlash
        user_data = validated_data.pop('user', {})  # user malumotlarini olish, ma'lumot bo'lmasa bo'sh dict
        # user uchun serializerni yaratish:
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():  # Agar user ma'lumotlari to'g'ri bo'lsa
            user_serializer.save()  # saqlash

        if 'group' in validated_data:
            instance.group.set(validated_data['group'])  # M2M uchun .set()

        instance.group.set(validated_data.get('group', instance.group.all()))  # guruhni yangilash
        instance.is_line = validated_data.get('is_line', instance.is_line)  # holatni yangilash
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)  # tavsif
        instance.save()  # saqlash
        return instance  # o'zgargan ma'lumotni qaytarish



# Parents modeli uchun serializer
class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents  # Qaysi model bilan ishlashini ko‘rsatadi
        # Seriyalizatsiya qilinadigan maydonlar
        fields = ['id', 'student', 'full_name', 'phone_number', 'address', 'descriptions']

