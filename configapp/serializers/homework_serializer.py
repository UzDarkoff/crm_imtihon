# serializers.py
from rest_framework import serializers
from ..models import Homework, HomeworkSubmission
from configapp.models import Teacher

class HomeworkSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'title', 'description', 'file', 'due_date', 'created_at', 'updated_at', 'is_submitted']

    def get_is_submitted(self, obj):
        teacher = self.context['request'].user.teacher_profile
        # Teacher can see homework for all students of their groups
        return obj.submissions.count() > 0

class HomeworkCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'file', 'due_date']

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = ['file', 'submitted_at']


