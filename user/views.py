from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User


class UserRegistration(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Account is created', status=200)
    
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    # def get(self, request):
    #     favorite = Favorite.objects.filter(owner=request.user).all()
    #     serializer = FavoriteSerializer(favorite, many=True)
    #     if serializer.data:
    #         return Response(serializer.data, 200)
    #     return Response('Нет избранных постов',204)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        response_data = {
            'token':token.key,
            'username':user.username,
            'id':user.id
        }
        return Response(response_data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('успешно вышли с аккаунта')


# написать UserListAPIView на generics запрос возвращает всех существующих ползователей
    
from .serializers import UserSerializer
from rest_framework import generics

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAdminUser]