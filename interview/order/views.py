from datetime import datetime

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


class ListBetweenStartEmbargoDates(generics.ListAPIView):
    """
    "Write an endpoint that lists orders that are between a particular start and embargo date."
    I had some difficulty understanding exactly what is being asked for here since an order has both
    a start date and an embargo date. I implemented it with my interpretation; however, I
    was also wondering if the question meant the API was expecting a date range for start date
    and a range for embargo date (4 different dates). I went with this implemenation as it was quicker...
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        start_date = datetime(
            self.kwargs["s_year"], self.kwargs["s_month"], self.kwargs["s_day"]
        )
        embargo_date = datetime(
            self.kwargs["e_year"], self.kwargs["e_month"], self.kwargs["e_day"]
        )
        return self.queryset.filter(start_date__gte=start_date).filter(
            embargo_date__lte=embargo_date
        )


class ListOrderTagsByOrder(generics.ListAPIView):
    serializer_class = OrderTagSerializer

    def get_queryset(self):
        return Order.objects.get(id=self.kwargs.get("id")).tags.all()


class ListOrdersByTag(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderTag.objects.get(id=self.kwargs.get("id")).orders.all()
