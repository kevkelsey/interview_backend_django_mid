from django.shortcuts import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Order
from .views import DeactivateOrder


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
