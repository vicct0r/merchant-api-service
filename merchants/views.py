from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, exceptions

from . import models
from . import serializers
from CustomMixins import TenantMixin, OwnershipPermissionMixin


class WorkplaceCreateAPIView(TenantMixin, generics.CreateAPIView):
    serializer_class = serializers.WorkplaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkplaceOwnerManagmentAPIView(TenantMixin, 
                                     OwnershipPermissionMixin, 
                                     generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.WorkplaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'


class WorkplacePublicAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.WorkplaceMinimalSerializer
    queryset = models.Workplace.objects.all()
    lookup_field = 'id'


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


        

