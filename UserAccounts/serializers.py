from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password')
    
    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is taken')
        return data
    def create(self, validated_data):
        user=CustomUser.objects.create(username=validated_data['username'],
                                 email=validated_data['email'],
                                 phone_number = validated_data['phone_number']
                                 )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account not found')
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return {'status': 0, 'message': 'Invalid credentials', 'data': {}}
        is_admin = int(user.is_staff) 
        refresh = RefreshToken.for_user(user)
        
        return {
            'status': 1,
            'message': 'Login success',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'is_admin': is_admin,
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')
        read_only_fields = ('username',)  # Assuming username is read-only

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

class EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields= ['username','id','first_name','last_name','email','phone_number']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number'] 