from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Har bir sahifada ko'rsatiladigan elementlar soni
    page_size_query_param = 'page_size'  # Foydalanuvchi sahifa o'lchamini belgilashi uchun
    max_page_size = 100  # Maksimal sahifa o'lchami
