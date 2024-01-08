from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from .views import *
from user.views import LoginView

class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.product = self.setUp_product()


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
    
    def setUp_product(self):
        data = {
            'name': 'car',
            'description': 'jhvmhjjh',
            'price': 50000,
            'quantity': 5,
        }
        request = self.factory.post('/product/', data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        view = ProductViewSet.as_view({'post':'create'})
        response = view(request)

        return response.data
    
    
    def test_product_get(self):
        request = self.factory.get('product/')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200

    def test_product_retrieve(self):
        response = self.client.get(f'/product/{self.product["id"]}/')

        self.assertEqual(response.status_code, 200)


    def test_product_post(self):
        data = {
            'name': 'car',
            'description': 'jhvmhjjh',
            'price': 50000,
            'quantity': 5,
        }
        request = self.factory.post('/product/', data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        view = ProductViewSet.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 201


    def test_product_put(self):
        updated_data = {
            'name': 'updated_name',
            'description': 'updated_descr',
            'price': 200,
            'quantity': 5,
        }
        response = self.client.put(f"/product/{self.product['id']}/", data=updated_data, HTTP_AUTHORIZATION=f'Token {self.token}')

        assert response.status_code == 200

    def test_product_patch(self):
        updated_data = {
            'price': 200,
            'quantity': 5,
        }
        response = self.client.patch(f"/product/{self.product['id']}/", data=updated_data, HTTP_AUTHORIZATION=f'Token {self.token}')
    
        assert response.status_code == 200

    def test_product_delete(self):
        response = self.client.delete(f"/product/{self.product['id']}/", HTTP_AUTHORIZATION=f'Token {self.token}')

        assert response.status_code == 204



    