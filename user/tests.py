from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from .views import *


# Create your tests here.

class UserTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()


    def setUp_user(self):
         return User.objects.create_superuser(username='test', password='1')
    
    def setUp_user_token(self):
        data = {
              'username' : 'test',
              'password': '1'
        }
        request = self.factory.post('user/login/', data)

        view = LoginView.as_view()
        response = view(request)

        return response.data['token']
    
    def test_get_user(self):
        request = self.factory.get('user/')
        view = UserListAPIView.as_view()
        response = view(request)

        assert response.status_code == 200

    def test_user_register(self):
        data = {
            'username': 'meerim',
            'first_name': 'Meerim',
            'last_name': 'meerim',
            'password': '123456789',
            'password_confirmation': '123456789'
        }
        request = self.factory.post('user/register/', data)
        view = UserRegistration.as_view()
        response = view(request)

        assert response.status_code == 200

    def test_user_login(self):
        request = self.factory.post('user/login/', {'username': 'test', 'password': '1'})
        view = LoginView.as_view()
        response = view(request)

        assert response.status_code == 200

    def test_user_logout(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)
        # Отправка POST-запроса на URL 'user/logout/'
        response = self.client.post('/user/logout/')

        # Проверка, что статус код ответа равен 200
        assert response.status_code == 200

    def test_user_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/user/{self.user.id}/')
        
        assert response.status_code == 200


        
