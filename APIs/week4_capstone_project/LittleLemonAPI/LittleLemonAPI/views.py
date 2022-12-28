from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import exceptions, viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .paginations import LargeResultsSetPagination, StandardResultsSetPagination
from .serializers import MenuItemModelSerializer, UserSerializer, CartSerializer, MenuItemSerializer, OrderItemSerializer, OrderSerializer
from .models import MenuItem, Cart, Order, OrderItem
import datetime
# Create your views here.


def isManager(user):
    return user.groups.filter(name='Manager').exists()


class MenuItemView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemModelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['category', 'price', 'featured']
    search_fields = ['title']
    ordering_fields = ['category', 'price']

    def get_permissions(self):
        user = self.request.user
        if self.request.method == 'POST':
            if user.is_superuser or isManager(user):
                return []
            else:
                raise exceptions.PermissionDenied()
        return []


class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemModelSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        user = self.request.user
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if user.is_superuser or isManager(user):
                return []
            else:
                raise exceptions.PermissionDenied()
        return []


class ManagerUserManagementView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):
        user = self.request.user
        if user.is_superuser or isManager(user):
            return []
        else:
            raise exceptions.PermissionDenied()

    def get(self, request):
        data = User.objects.filter(groups__name='Manager')
        ser_data = UserSerializer(data, many=True).data
        return Response(ser_data, 200)

    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            Group.objects.get(name='Manager').user_set.add(user)
        except User.DoesNotExist:
            return Response({}, 404)
        return Response({}, 201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def RemoveManagerUserGroup(request, pk=None):
    if request.user.is_superuser or isManager(request.user):
        try:
            user = User.objects.get(pk=pk)
            Group.objects.get(name='Manager').user_set.remove(user)
        except User.DoesNotExist:
            return Response({}, 404)
        return Response({}, 200)
    else:
        return Response({'details': 'you are not authorized to do such action'}, 403)


class DeliveryCrewUserManagementView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):
        user = self.request.user
        if user.is_superuser or isManager(user):
            return []
        else:
            raise exceptions.PermissionDenied()

    def get(self, request):
        data = User.objects.filter(groups__name='Delivery crew')
        ser_data = UserSerializer(data, many=True).data
        return Response(ser_data, 200)

    def post(self, request):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            Group.objects.get(name='Delivery crew').user_set.add(user)
        except User.DoesNotExist:
            return Response({}, 404)
        return Response({}, 201)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def RemoveDeliveryCrewUserGroup(request, pk=None):
    if request.user.is_superuser or isManager(request.user):
        try:
            user = User.objects.get(pk=pk)
            Group.objects.get(name='Delivery crew').user_set.remove(user)
        except User.DoesNotExist:
            return Response({}, 404)
        return Response({}, 200)
    else:
        return Response({'details': 'you are not authorized to do such action'}, 403)


class CartView(ListCreateAPIView, DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response({}, 200)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['date', 'status', 'user__username']
    search_fields = ['date']
    ordering_fields = ['date', 'total']

    def get(self, request):
        user = request.user
        context = {}
        if isManager(user) or user.is_superuser:
            orders = Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(user=request.user)

        for order in orders:
            ser_order = OrderSerializer(order).data
            orderitems = order.orderitem_set.all()
            ser_menuitems = OrderItemSerializer(orderitems, many=True).data
            context['order_details'] = {
                'order': ser_order,
                'menu_items': ser_menuitems
            }
        return Response(context, 200)

    def post(self, request):
        user = request.user
        date = datetime.date.today()
        order = Order.objects.create(user=user, date=date, total=0.0)
        cart_items = Cart.objects.filter(user=user)
        total = 0.0
        for cart_item in cart_items:
            total += float(int(cart_item.quantity) *
                           float(cart_item.unit_price))
            OrderItem.objects.create(
                order=order,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price,
                menuitem=cart_item.menuitem)
        order.total = total
        order.save()
        cart_items.delete()
        return Response({}, 201)


class SingleOrderView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        user = self.request.user
        if self.request.method == "DELETE":
            if user.is_superuser or isManager(user):
                return []
            else:
                raise exceptions.PermissionDenied()
        if self.request.method == "GET":
            if user.groups.filter(name='Customer').exists():
                return []
            else:
                raise exceptions.PermissionDenied()
        if self.request.method == 'PATCH':
            if user.groups.filter(name__in=['Delivery crew', 'Manager']).exists():
                return []
            else:
                raise exceptions.PermissionDenied()
        if self.request.method == 'PUT':
            if user.groups.filter(name='Manager').exists():
                return []
            else:
                raise exceptions.PermissionDenied()

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        if request.user != order.user:
            return Response({}, 403)

        order_items = order.orderitem_set.all()
        print(order_items)
        menu_items = []
        for order_item in order_items:
            menu_items.append(order_item.menuitem)
        menu_items = MenuItemModelSerializer(menu_items, many=True).data
        return Response(menu_items, 200)

    def put(self, request, pk):
        order = Order.objects.get(pk=pk)
        status = request.POST.get('status')
        if status:
            order.status = True
        delivery_crew_id = request.POST.get('delivery_crew_id')
        if delivery_crew_id:
            delivery_crew = User.objects.get(id=delivery_crew_id)
            order.delivery_crew = delivery_crew
        order.save()
        return Response({}, 201)

    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        status = request.POST.get('status')
        if status:
            order.status = True
        if isManager(request.user) or request.user.is_superuser:
            delivery_crew_id = request.POST.get('delivery_crew_id')
            if delivery_crew_id:
                delivery_crew = User.objects.get(id=delivery_crew_id)
                order.delivery_crew = delivery_crew
        order.save()
        return Response({}, 201)

    def delete(self, request, pk):
        Order.objects.get(pk=pk).delete()
        return Response({}, 200)
