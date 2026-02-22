from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import WorkplaceCreationSerializer, InviteJoinWorkplace


class WorkplaceCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkplaceCreationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JoinAsMerchantAPIView(generics.CreateAPIView):
    serializer_class = InviteJoinWorkplace
    queryset = models.MerchantStaffProfile

    def perform_create(self, serializer):
        if not self.kwargs.get('invite'):
            return Response(serializer.errors)
        serializer.save(user=self.request.user, workplace=self.kwargs.get('invite'))
        
