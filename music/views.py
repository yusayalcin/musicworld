from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from music.models import UserExtended, Music
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import filters, generics
from django.shortcuts import get_object_or_404

from .serializers import *


class RegisterView(APIView):

    def post(self, request):
        request_data = request.data
        ser = UserSerializer(data=request_data)
        if ser.is_valid():
            user = UserExtended.objects.create_user(**ser.validated_data)
            login(request, user)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class LoginView(APIView):

    def post(self, request):
        request_data = request.data
        ser = LoginSerializer(data=request_data)
        if ser.is_valid():
            user = authenticate(
                request, username=ser.validated_data["username"], password=ser.validated_data["password"])
            if user is not None:
                login(request, user)
                ser = UserSerializer(user)
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response("credentials invalid", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# This view is for rating
# This view should return an average (mean) of all the rating of different Users for a specific Music
class RatingView(APIView):

    # gets the average of ratings for a specific music
    def get(self, request, title):
        music = get_object_or_404(Music, title=title)
        return Response({"rate": music.rating}, status=status.HTTP_200_OK)

    # handles the rating of a music by a specific user
    def post(self, request):
        ser = RatingSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        print(ser.validated_data)

        music = get_object_or_404(Music, title=ser.validated_data['title'])
        user = UserExtended.objects.get(username=ser.validated_data['username'])
        rate = Rating(score=ser.validated_data['score'])
        rate.save()
        rate.musics.set([music])
        rate.users.set([user])

        return Response(status=status.HTTP_201_CREATED)


# This view is for creating and updating and deleting a music
class MusicView(APIView):
    # getting
    def get(self, request, format=None):
        songs = Music.objects.all()
        ser = MusicSerializer(songs, many=True)
        return Response(ser.data)

    # creating
    def post(self, request):
        request_data = request.data
        ser = MusicSerializer(data=request_data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Returns a music object for updating/deleting
    def get_object(self, title):
        try:
            return Music.objects.get(title=title)
        except Music.DoesNotExist:
            raise Http404

    # updating
    def put(self, request, title):
        request_data = request.data
        music = self.get_object(title=title)
        ser = MusicSerializer(music, data=request_data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    # deleting
    def delete(self, request, title):
        music = self.get_object(title=title)
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# This view is for both Searching and filtering
# return a list containing Music Objects

class SearchView(generics.ListCreateAPIView):

    search_fields = ['title', 'singer']
    filter_backends = (filters.SearchFilter,)
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
