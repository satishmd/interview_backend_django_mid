from datetime import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
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


class DeactivateOrderView(APIView):

    def patch(self, request: Request, *args, **kwargs) -> Response:
        order_id = kwargs.get("id")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=404)
        
        order.is_active = False

        order.save(update_fields=["is_active"])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
