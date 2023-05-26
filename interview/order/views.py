from django.shortcuts import render
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrder(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        order: Order = self.get_object()
        if not order.is_active:
            raise ValidationError("Order is already deactivated")
        Order.deactivate(order.id)
        order.refresh_from_db()
        serializer = self.get_serializer_class()(order)
        return Response(data=serializer.data)
