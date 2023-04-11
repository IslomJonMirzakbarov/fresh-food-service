from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('categories/<int:pk>', views.CategoryRetrieveUpdateDestroyView.as_view(),
         name='category-retrieve-udpate-destroy'),

    path('menu-items/', views.MenuItemListCreateView.as_view(),
         name='menu-item-list-create'),
    path('menu-items/<int:pk>', views.MenuItemRetrieveUpdateDestroyView.as_view(),
         name='menu-item-retrieve-update-destroy'),

    path('carts/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>', views.CartRetrieveUpdateDestroyView.as_view(),
         name='cart-retrieve-update-destroy'),

    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', views.OrderRetrieveUpdateDestroyView.as_view(),
         name='order-retrieve-update-destroy'),

    path('order-items/', views.OrderItemListCreateView.as_view(),
         name='order-item-list-create'),
    path('order-items/<int:pk>', views.OrderItemRetrieveUpdateDestroyView.as_view(),
         name='order-item-retrieve-update-destroy'),

    path('groups/manager/users/', views.UserGroupManagement.as_view(
        group_name='Manager'), name='manager-group-management'),
    path('groups/manager/users/<int:user_id>/', views.UserGroupManagement.as_view(
        group_name='Manager'), name='manager-group-management-delete'),
    path('groups/delivery-crew/users/', views.UserGroupManagement.as_view(
        group_name='Delivery crew'), name='delivery-crew-group-management'),
    path('groups/delivery-crew/users/<int:user_id>/', views.UserGroupManagement.as_view(
        group_name='Delivery crew'), name='delivery-crew-group-management-delete'),
]
