from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersByTagListView


urlpatterns = [
    path("tags/", OrderTagListCreateView.as_view(), name="order-tag-list-create"),
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path("tags/<int:tag_id>/orders/", OrdersByTagListView.as_view(), name="tag-orders-list"),

]
