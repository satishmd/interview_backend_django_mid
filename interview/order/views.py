from django.shortcuts import render,get_object_or_404
from datetime import datetime

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        start_date = self.request.query_params.get("start_date")
        embargo_date = self.request.query_params.get("embargo_date")

        if start_date and embargo_date:
            parsed_start = self.parse_date(start_date)
            parsed_embargo = self.parse_date(embargo_date)

            if parsed_start > parsed_embargo:
                raise ValidationError(
                    {"error": "start_date cannot be after embargo_date."}
                )

            queryset = queryset.filter(
                start_date__gte=parsed_start,
                embargo_date__lte=parsed_embargo,
            )

        return queryset

    @staticmethod
    def parse_date(value: str):
        if not value:
            raise ValidationError({"error": "Date cannot be empty."})

        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            raise ValidationError(
                {"error": "Date must be in ISO 8601 format (YYYY-MM-DD)."}
            )

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class OrdersByTagListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tag = get_object_or_404(OrderTag, pk=self.kwargs["tag_id"])
        return tag.orders.all()

class OrderTagsByOrderListView(generics.ListAPIView):
    serializer_class = OrderTagSerializer

    def get_queryset(self):
        order = get_object_or_404(Order, pk=self.kwargs["order_id"])
        return order.tags.all()

class DeactivateOrderView(APIView):
    def patch(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, pk=id)
        order.is_active = False
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)
