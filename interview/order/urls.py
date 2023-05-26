from django.urls import path

from .views import (
    DeactivateOrder,
    ListBetweenStartEmbargoDates,
    OrderListCreateView,
    OrderTagListCreateView,
)

urlpatterns = [
    path(
        "list/start/<int:s_year>/<int:s_month>/<int:s_day>/embargo/<int:e_year>/<int:e_month>/<int:e_day>/",
        ListBetweenStartEmbargoDates.as_view(),
        name="start-embargo-list",
    ),
    path("deactivate/<int:id>/", DeactivateOrder.as_view(), name="deactivate-order"),
    path("tags/", OrderTagListCreateView.as_view(), name="order-detail"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
