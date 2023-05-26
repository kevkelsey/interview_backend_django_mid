from django.shortcuts import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from .views import InventoryListByCreatedAfterDate, InventoryListCreateView


class GetInventoryCreatedAfterDate(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = InventoryListByCreatedAfterDate.as_view()

    def test_created_by_list(self):
        request = self.factory.get(
            reverse(
                "inventory-created-after", kwargs={"year": 2023, "month": 5, "day": 19}
            )
        )
        response = self.view(request, year=2023, month=5, day=19)
        assert len(response.data) >= 17
        assert response.status_code == 200


class TestListViewPagination(APITestCase):
    fixtures = ["fixtures/test_data.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = InventoryListCreateView.as_view()

    def test_response_is_paginated(self):
        request = self.factory.get(reverse("inventory-list"))
        response = self.view(request)
        self.assertEqual(len(response.data.get("results")), 3)
