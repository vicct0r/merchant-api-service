from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from . import models
from .serializers import ProductCatalogSerializer, ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        workplace = self.request.user.workplace
        if not workplace:
            return Response({'detail': 'Could not find any workplace.'}, status=404)
        return models.Product.objects.filter(workplace=workplace)
    # Isso aqui nao vai funcionar, temos uma relacao fragil entre Workplace - User - Owner
    # Refatorar este trecho em cima da nova modelagem
    