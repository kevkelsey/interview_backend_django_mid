from django.shortcuts import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from .views import InventoryListByCreatedAfterDate


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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 17)
