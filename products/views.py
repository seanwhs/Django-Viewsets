# products/views.py
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ViewSet):
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]  # public
        return [IsAuthenticated()]  # JWT required for all other actions

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug=None):  # Fixed parameter
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, slug=None):  # Fixed parameter
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, slug=None):  # Fixed parameter
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, slug=None):  
        product = get_object_or_404(Product, slug=slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
