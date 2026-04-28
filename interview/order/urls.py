from django.urls import path
from interview.order.views import (
    OrderListCreateView,
    OrderTagListCreateView,
    OrderTagsByOrderListView,
)


urlpatterns = [
    path("<int:order_id>/tags/", OrderTagsByOrderListView.as_view(), name="order-tags-list"),
    path("tags/", OrderTagListCreateView.as_view(), name="order-tags-list-create"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
