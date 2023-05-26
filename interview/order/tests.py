from datetime import datetime

from django.shortcuts import reverse
from interview.inventory.models import Inventory
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Order
from .views import (
    DeactivateOrder,
    ListBetweenStartEmbargoDates,
    ListOrdersByTag,
    ListOrderTagsByOrder,
)


class TestDeactivateOrder(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = DeactivateOrder.as_view()
        self.order = Order.objects.get(id=1)

    def test_successful_deactivation(self):
        self.assertTrue(self.order.is_active)
        request = self.factory.patch(reverse("deactivate-order", kwargs={"id": "1"}))
        response = self.view(request, pk=1)
        self.assertFalse(response.data.get("is_active"))

    def test_already_deactivated(self):
        self.order.deactivate(self.order.id)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
        request = self.factory.patch(reverse("deactivate-order", kwargs={"id": "1"}))
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 400)


class TestListBetweenStartEmbargoDates(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ListBetweenStartEmbargoDates.as_view()
        date1 = datetime(2023, 5, 21)
        date2 = datetime(2023, 5, 26)
        date3 = datetime(2023, 5, 30)
        self.inventory1 = Inventory.objects.get(id=1)
        self.inventory2 = Inventory.objects.get(id=2)
        self.orders = [
            Order.objects.create(
                inventory=self.inventory1, start_date=date1, embargo_date=date2
            ),
            Order.objects.create(
                inventory=self.inventory2, start_date=date2, embargo_date=date3
            ),
        ]

    def test_get_both_orders(self):
        request = self.factory.get(
            reverse(
                "start-embargo-list",
                kwargs={
                    "s_year": 2023,
                    "s_month": 5,
                    "s_day": 21,
                    "e_year": 2023,
                    "e_month": 5,
                    "e_day": 30,
                },
            )
        )
        response = self.view(
            request, s_year=2023, s_month=5, s_day=21, e_year=2023, e_month=5, e_day=30
        )
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)


class TestListOrderTagsByOrder(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ListOrderTagsByOrder.as_view()

    def test_order_tags_view(self):
        request = self.factory.get(
            reverse("list-order-tags-by-order", kwargs={"id": 1})
        )
        response = self.view(request, id=1)
        self.assertEqual(len(response.data), 3)


class TestListOrdersByTag(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ListOrdersByTag.as_view()

    def test_list_all_orders_by_tag(self):
        request = self.factory.get(reverse("list-orders-by-tag", kwargs={"id": 17}))
        response = self.view(request, id=17)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
