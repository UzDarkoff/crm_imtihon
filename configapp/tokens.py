from rest_framework_simplejwt.tokens import RefreshToken

# Token yaratish funksiyasi
def create_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
