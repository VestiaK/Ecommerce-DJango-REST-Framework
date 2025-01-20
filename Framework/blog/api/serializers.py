from typing import Self
from urllib import request
from flask import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from streamlit import status
from .models import *

# Serializer untuk Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
# Serializer untuk CartItem
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Menyertakan informasi produk

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

# Serializer untuk Cart
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

# Serializer untuk OrderItem
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

# Serializer untuk Order
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price', 'items']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user