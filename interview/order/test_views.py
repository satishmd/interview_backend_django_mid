from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryType,
)
from interview.order.models import Order


class DeactivateOrderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create required inventory data
        self.inventory_type = InventoryType.objects.create(name="Movie")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        self.inventory = Inventory.objects.create(
            name="Test Movie",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 2020,
                "actors": ["Actor Name"],
                "imdb_rating": 7.5,
                "rotten_tomatoes_rating": 80,
            },
        )

        # Create an active order
        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-04-27",
            embargo_date="2026-05-27",
            is_active=True,
        )

    def test_deactivate_order_success(self):
        """Test successfully deactivating an active order"""
        url = f"/orders/{self.order.id}/deactivate/"
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_active"])
        # Refresh from database
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)

    def test_deactivate_order_not_found(self):
        """Test deactivating a non-existent order returns 404"""
        url = "/orders/9999/deactivate/"
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 404)
