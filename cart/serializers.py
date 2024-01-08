from rest_framework import serializers
from .models import Cart

class CartSeralizers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Cart
        fields = '__all__'


