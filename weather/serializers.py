from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WeatherRecord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class WeatherRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields = [
            'id', 'user', 'location', 'temperature', 'feels_like',
            'description', 'icon_url', 'humidity', 'wind',
            'date_recorded', 'latitude', 'longitude', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
