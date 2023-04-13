from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from djoser.serializers import UserSerializer
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price')


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('order', 'menuitem', 'quantity', 'unit_price', 'price')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status',
                  'total', 'date', 'order_items')
        read_only_fields = ('total',)

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.price for item in cart_items)

        validated_data['user'] = user
        validated_data['total'] = total
        order = super().create(validated_data)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            )
        cart_items.delete()

        return order


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
