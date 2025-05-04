from django.db import models
from .student_model import Student

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # To'lov miqdori
    date = models.DateField(auto_now_add=True)  # To'lov sanasi
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')  # To'lov holati

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.amount} - {self.status}"
