from django.urls import path
from interview.order.views import (
    DeactivateOrderView,
    OrderListCreateView,
    OrderTagListCreateView,
)


urlpatterns = [
    path("tags/", OrderTagListCreateView.as_view(), name="order-tags-list"),
    path(
        "<int:id>/deactivate/",
        DeactivateOrderView.as_view(),
        name="order-deactivate",
    ),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
