from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, views, status, response
from .models import Category, Cart, MenuItem, Order, OrderItem
from .serializers import CategorySerializer, CartSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager, IsDeliveryCrew


class UserGroupManagement(views.APIView):
    def get(self, request, group_name):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        group = get_object_or_404(Group, name=group_name)
        users = group.user_set.all()
        user_data = [{'id': user.id, 'username': user.username}
                     for user in users]
        return response.Response(user_data, status=status.HTTP_200_OK)

    def post(self, request, group_name):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        group = Group.objects.get_or_create(name=group_name)[0]
        group.user_set.add(user)
        return response.Response(status=status.HTTP_201_CREATED)

    def delete(self, request, group_name, user_id):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, name=group_name)
        group.user_set.remove(user)
        return response.Response(status=status.HTTP_200_OK)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class MenuItemRetrieveUpdateDestroyView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer()


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
