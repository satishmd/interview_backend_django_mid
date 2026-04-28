from django.shortcuts import render,get_object_or_404
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderTagsByOrderListView(generics.ListAPIView):
    serializer_class = OrderTagSerializer

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs["order_id"])
        return order.tags.all()

