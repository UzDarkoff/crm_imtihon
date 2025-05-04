
from .group_model import *

class Lesson(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lessons')
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f"{self.subject} - {self.teacher.user.phone_number} - {self.date}"
