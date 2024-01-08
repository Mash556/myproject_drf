from rest_framework import viewsets
from rest_framework import permissions

from .serializers import CategorySerializers
from .models import Category
from .permissions import IsOwner


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.OR(permissions.IsAdminUser(), IsOwner())]
        return [permissions.IsAuthenticatedOrReadOnly()] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
