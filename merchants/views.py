from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import WorkplaceCreationSerializer


class WorkplaceCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkplaceCreationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        
