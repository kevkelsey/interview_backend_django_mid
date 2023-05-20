from django.shortcuts import reverse

from rest_framework.test import APIRequestFactory, APITestCase


from .models import Inventory
from .views import InventoryListByCreatedAfterDate

from datetime import datetime

class GetInventoryCreatedAfterDate(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view =  InventoryListByCreatedAfterDate.as_view()

    def test_created_by_list(self):
        request = self.factory.get(reverse('inventory-created-after', kwargs={'year': 2023, 'month': 5, 'day': 19}))
        response = self.view(request, year=2023, month=5, day=19)
        assert response.status_code == 200
