from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Cart
from .serializers import CartSeralizers
from .permissions import IsOwnerOrAdminReadOnly

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSeralizers
    # lookup_field = 'id'

    def get_permissions(self):
        if self.request.method != 'POST':
            return [IsOwnerOrAdminReadOnly()]
        return [permissions.IsAuthenticated()]

    
    def perform_create(self, serializer):
        user = self.request.user

        # Проверяем, существует ли уже объект корзины для данного пользователя
        existing_cart = Cart.objects.filter(user=user).first()

        if existing_cart:
            # Если корзина уже существует, вы можете обновить ее или вернуть ошибку, в зависимости от требований вашего приложения
            serializer.update(existing_cart, serializer.validated_data)
        else:
            # Если корзины для данного пользователя нет, создайте новую
            serializer.save(user=user)