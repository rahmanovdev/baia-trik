from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'data', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверный учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    data = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age', 'phone_number', 'data']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CarSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_name']


class CarListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    add_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Car
        fields = ['id', 'car_name', 'add_date', 'country', 'average_rating', 'image']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class CarDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    add_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    ratings = serializers.SerializerMethodField()
    owner = UserProfileSimpleSerializer()

    class Meta:
        model = Car
        fields = ['id', 'owner', 'car_name', 'description', 'year', 'price', 'add_date', 'country',
                  'mileage', 'with_photo', 'volume', 'image', 'condition', 'customs',
                  'availability', 'body', 'color', 'registration', 'ratings', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_ratings(self, obj):
        ratings = Rating.objects.filter(car=obj)
        return RatingSerializer(ratings, many=True).data


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    car = CarSimpleSerializer()

    class Meta:
        model = Rating
        fields = ['user', 'car', 'parent', 'text', 'created_date']


class FavoriteCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCar
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
