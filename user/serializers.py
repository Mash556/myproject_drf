from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    password_confirmation = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation']

    
    def validate(self, attrs):
        password_conf = attrs.pop('password_confirmation')
        if password_conf != attrs['password']:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError(
                'Имя должно начинатся с заглавной буквы'
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        request = self.context.get('request')
        if username and password:
            user = authenticate(
                username=username,
                password=password,
                request=request
            )
            if not user:
                raise serializers.ValidationError(
                    'Не правильный пароль или юзернейм'
                )
        else:
            raise serializers.ValidationError(
                'Вы забыли запонить username или password'
            )
        data['user'] = user
        return data
    
    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'username not found'
            )
        return username
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User