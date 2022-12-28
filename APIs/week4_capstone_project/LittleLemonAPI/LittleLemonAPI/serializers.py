from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class MenuItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class MenuItemSerializer(serializers.Serializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
        }


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        user = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all().all,
            default=serializers.CurrentUserDefault()
        )


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = ['user', 'user_id', 'delivery_crew',
                  'status', 'total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemModelSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
