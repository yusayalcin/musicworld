from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExtended
        fields = ["username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserExtended
        fields = ["username", "password"]
        extra_kwargs = {
            "username": {'validators': None},
        }


class RatingSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    class Meta:
        model = Rating

        fields = ["score", "title", "username"]


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ["title","singer","date_of_post","music_file"]
