from rest_framework import serializers
from .models import Category


class CategorySerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Category
        fields = '__all__'
