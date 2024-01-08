from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User
from .views import *
from user.views import LoginView
from product.views import ProductViewSet
# from rest_framework.test import force_authenticate

class CartTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.product = self.setUp_product()
        self.cart = self.setUp_cart()

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
    
    def setUp_cart(self):
        data = {'product': self.product['id']}
        request = self.factory.post('cart/', data=data, HTTP_AUTHORIZATION='Token '+self.token)
        view = CartViewSet.as_view({'post': 'create'})
        response = view(request)
        return response.data
    
    def test_cart_post(self):
        data = {'product': self.product['id']}
        request = self.factory.post('cart/', data=data, HTTP_AUTHORIZATION='Token '+self.token)
        view = CartViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == 201

    def test_cart_get(self):
        request = self.factory.get('cart/', HTTP_AUTHORIZATION='Token '+self.token)
        view = CartViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200

    def test_cart_get(self):
        response = self.client.get(f'/cart/{self.cart["id"]}/', HTTP_AUTHORIZATION='Token '+self.token)

        assert response.status_code == 200

    def test_cart_path(self):
        response = self.client.patch(f'/cart/{self.cart["id"]}/', data={'quantity': 3}, HTTP_AUTHORIZATION='Token '+self.token)

        assert response.status_code == 200

    def test_cart_put(self):
        response = self.client.put(f'/cart/{self.cart["id"]}/', data={'product': self.cart['id'] ,'quantity': 10}, HTTP_AUTHORIZATION='Token '+self.token)

        assert response.status_code == 200

    def test_cart_delete(self):
        response = self.client.delete(f'/cart/{self.cart["id"]}/', HTTP_AUTHORIZATION='Token '+self.token)

        assert response.status_code == 204
    

    # def test_cart_delete(self):
    #     request = self.factory.delete(f'/cart/{self.cart["id"]}/', HTTP_AUTHORIZATION='Token '+self.token)
    #     view = CartViewSet.as_view({'delete': 'destroy'})
    #     response = view(request)

    #     assert response.status_code == 204 