from rest_framework import serializers

class AttendanceItemSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=['present', 'late', 'absent'])

class GroupAttendanceGETResponseSerializer(serializers.Serializer):
    attendance_data = AttendanceItemSerializer(many=True)
