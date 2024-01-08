from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from .views import *
from user.views import LoginView

class CategoryTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.category = self.setUp_category()

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
    
    def setUp_category(self):
        request = self.factory.post('category/', data={'name': 'bluzka'}, HTTP_AUTHORIZATION='Token '+self.token)
        view = CategoryViewSet.as_view({'post': 'create'})
        response = view(request)
        return response.data
    
    def test_category_get(self):
        request = self.factory.get('category/')
        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200


    def test_category_retrieve(self):
        response = self.client.get(f'/category/{self.category["id"]}/')

        self.assertEqual(response.status_code, 200)


    def test_category_post(self):
        request = self.factory.post('category/', data={'name': 'bluzka'}, HTTP_AUTHORIZATION='Token '+self.token)
        view = CategoryViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == 201

    def test_category_put(self):
        response = self.client.put(f'/category/{self.category["id"]}/', data={'name': 'djins'}, HTTP_AUTHORIZATION='Token '+self.token)

        self.assertEqual(response.status_code, 200)

    def test_category_delete(self):
        response = self.client.delete(f'/category/{self.category["id"]}/', HTTP_AUTHORIZATION='Token '+self.token)

        assert response.status_code == 204