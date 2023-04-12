from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, views, status, response, filters
from .models import Category, Cart, MenuItem, Order, OrderItem
from .serializers import CategorySerializer, CartSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager, IsDeliveryCrew


class UserGroupManagement(views.APIView):
    group_name = None

    def get(self, request, *args, **kwargs):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        group = get_object_or_404(Group, name=self.group_name)
        users = group.user_set.all()
        user_data = [{'id': user.id, 'username': user.username}
                     for user in users]
        return response.Response(user_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        group = Group.objects.get_or_create(name=self.group_name)[0]
        group.user_set.add(user)
        return response.Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if not IsManager().has_permission(request, self):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, name=self.group_name)
        group.user_set.remove(user)
        return response.Response(status=status.HTTP_200_OK)


class CartManagement(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        user_carts = self.request.get_queryset()
        user_carts.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username',
                     'delivery_crew__username', 'status', 'date']
    ordering_fields = ['user', 'delivery_crew', 'status', 'total', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        total = sum(item.price for item in cart_items)
        order = serializer.save(user=user, total=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            )
        cart_items.delete()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            if self.request.user.groups.filter(name='Delivery crew').exists():
                self.permission_classes = [IsDeliveryCrew]
            else:
                self.permission_classes = [IsManager]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if user.groups.filter(name='Delivery crew').exists():
            if 'status' in request.data:
                order.status = request.data['status']
                order.save()
                return response.Response(status=status.HTTP_200_OK)
            else:
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category_name']
    ordering_fields = ['name', 'price', 'category']

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
