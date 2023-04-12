from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from djoser.serializers import UserSerializer
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all())
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2)

    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    model = Order
    fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    model = OrderItem
    fields = '__all__'


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
