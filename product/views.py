from rest_framework import viewsets
from rest_framework import permissions


from .serializers import ProductSerializers
from .models import Category, Product
from .permissions import IsOwner


class ProductViewSet(viewsets.ModelViewSet):
    # lookup_field = 'id'  # это поле по которой будет 

    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.OR(permissions.IsAdminUser(), IsOwner())]
        return [permissions.IsAuthenticatedOrReadOnly()] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




