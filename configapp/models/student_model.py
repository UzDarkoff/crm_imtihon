from .auth_user import *
class Student(BaseModel):
    STATUS_CHOICES = (
        ('ongoing', 'Oʻqiyotgan'),
        ('graduated', 'Bitirgan'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    group = models.ManyToManyField('GroupStudent', related_name='students_group')
    is_line = models.BooleanField(default=False)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone_number


class Parents(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent')
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.full_name
