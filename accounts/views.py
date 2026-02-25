from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions, authentication

from .models import CustomUser
from .serializers import CustomUserSignupSerializer, CustomUserSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSignupSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    