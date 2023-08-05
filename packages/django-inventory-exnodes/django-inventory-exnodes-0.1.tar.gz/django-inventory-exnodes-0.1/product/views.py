from django.shortcuts import render
from rest_framework import views, generics
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework.response import Response

# Create your views here.
class GetCreateProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        print(serializer.data)
        response = {}
        response['data'] = serializer.data
        return Response(response)
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ProductSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {}
        response['data'] = serializer.data
        return Response(response)