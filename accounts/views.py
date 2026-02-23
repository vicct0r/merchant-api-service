from django.shortcuts import render
from rest_framework import generics

from .models import CustomUser
from .serializers import CustomUserSignupSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSignupSerializer
    queryset = CustomUser.objects.all()
