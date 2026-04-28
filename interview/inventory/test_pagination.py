from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


class InventoryPaginationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/inventory/"
        self.inventory_type = InventoryType.objects.create(name="Movie")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        self.metadata = {
            "year": 2024,
            "actors": ["Actor One"],
            "imdb_rating": 8.1,
        }

        for i in range(5):
            Inventory.objects.create(
                name=f"Inventory {i + 1}",
                type=self.inventory_type,
                language=self.inventory_language,
                metadata=self.metadata,
            )

    def test_inventory_list_default_pagination_returns_three_items(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(response.data["offset"], 0)
        self.assertEqual(response.data["limit"], 3)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"][0]["name"], "Inventory 1")

    def test_inventory_list_pagination_with_offset_returns_remaining_items(self):
        response = self.client.get(self.url, {"offset": 3, "limit": 3})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(response.data["offset"], 3)
        self.assertEqual(response.data["limit"], 3)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Inventory 4")
