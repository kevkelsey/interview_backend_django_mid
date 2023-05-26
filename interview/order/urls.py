from django.urls import path

from .views import DeactivateOrder, OrderListCreateView, OrderTagListCreateView

urlpatterns = [
    path("deactivate/<int:id>/", DeactivateOrder.as_view(), name="deactivate-order"),
    path("tags/", OrderTagListCreateView.as_view(), name="order-detail"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
