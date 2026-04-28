from django.shortcuts import render,get_object_or_404
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class OrdersByTagListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tag = get_object_or_404(OrderTag, pk=self.kwargs["tag_id"])
        return tag.orders.all()
