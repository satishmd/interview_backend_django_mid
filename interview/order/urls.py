from django.urls import path
from interview.order.views import (
    OrderListCreateView,
    OrderTagListCreateView,
    OrderTagsByOrderListView,
    DeactivateOrderView,
    OrderListCreateView,
    OrderTagListCreateView,
)


urlpatterns = [
    path("<int:order_id>/tags/", OrderTagsByOrderListView.as_view(), name="order-tags-list"),
    path("tags/", OrderTagListCreateView.as_view(), name="order-tags-list-create"),
    path(
        "<int:id>/deactivate/",
        DeactivateOrderView.as_view(),
        name="order-deactivate",
    ),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
