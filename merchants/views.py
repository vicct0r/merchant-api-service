from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, exceptions
from django.contrib.auth import get_user_model

from . import models
from . import serializers
from CustomMixins import TenantMixin, OwnershipPermissionMixin

User = get_user_model()

class WorkplaceCreateAPIView(TenantMixin, generics.CreateAPIView):
    serializer_class = serializers.WorkplaceSerializer

    def perform_create(self, serializer):
        workplace = serializer.save(owner=self.request.user)
        user = self.request.user
        user.workplace = workplace
        user.save(update_fields=["workplace"])
        

class WorkplaceOwnerManagmentAPIView(TenantMixin, 
                                     OwnershipPermissionMixin, 
                                     generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WorkplaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        user = self.request.user
        if not user.workplace:
            raise exceptions.ValidationError('You do not have a workplace.')
        return user.workplace


class WorkplacePublicAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.WorkplaceMinimalSerializer
    queryset = models.Workplace.objects.all()
    lookup_field = 'id'
    permission_classes = []
    authentication_classes = []


class WorkplaceInvitationAPIView(APIView):
    """
    - Method: POST
    - Parameters: workplace_id
    - Description: User is able to join to the workplace if he is on the whitelist.
    """
    def post(self, request):
        serializer = serializers.InviteToWorkplaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        workplace = get_object_or_404(models.Workplace, id=data['workplace_id'])

        if not request.user in workplace.whitelist.all():
            raise exceptions.ValidationError('You are not allowed to join this workplace.')
        
        workplace.whitelist.add(request.user)
        return Response(serializer.data)


class WorkplaceAddUserAPIView(APIView):
    def post(self, request):
        serializer = serializers.WhitelistAddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['user']

        user = get_object_or_404(User, email=email)

        if not request.user.workplace:
            raise exceptions.ValidationError('You do not have a workplace attached to your account.')
        if not request.user == request.user.workplace.owner:
            raise exceptions.ValidationError('You can not perform this action.')
        
        workplace = request.user.workplace
        workplace.whitelist.add(user)
        return Response(serializer.data)
