from django.urls import path, include
from .views import MenuItemView, SingleMenuItemView, ManagerUserManagementView, RemoveManagerUserGroup, DeliveryCrewUserManagementView, RemoveDeliveryCrewUserGroup, CartView, OrderView,SingleOrderView
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/users/me/', include('djoser.urls'), name='user-detail'),

    path('menu-items', MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(),
         name='single-menu-item'),

    path('groups/manager/users', ManagerUserManagementView.as_view(),
         name='managers-user-management'),
    path('groups/manager/users/<int:pk>',
         RemoveManagerUserGroup, name='remove-manager'),

    path('groups/delivery-crew/users', DeliveryCrewUserManagementView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', RemoveDeliveryCrewUserGroup),

    path('cart/menu-items', CartView.as_view()),
    path('orders', OrderView.as_view(), name='orders'),
    path('orders/<int:pk>',SingleOrderView.as_view(), name='order-details'),
]
