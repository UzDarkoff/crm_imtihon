from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.payment_model import Payment
from ..serializers.payment_serializer import PaymentSerializer
from ..permissions import  IsAdminOrStaffOrStudentOrTeacher


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrStaffOrStudentOrTeacher]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            # O'qituvchi o'z guruhidagi talabalarning to'lovlarini ko'rishi mumkin
            return Payment.objects.filter(student__group__teacher__user=user)
        elif user.is_student:
            # Talaba faqat o'z to'lovlarini ko'rishi mumkin
            return Payment.objects.filter(student__user=user)
        return Payment.objects.all()
