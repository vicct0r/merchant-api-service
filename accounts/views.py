from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from .models import CustomUser
from .serializers import CustomUserSignupSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSignupSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
