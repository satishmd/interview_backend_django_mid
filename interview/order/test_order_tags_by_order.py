from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order, OrderTag


class OrderTagsByOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.inventory_type = InventoryType.objects.create(name="Movie")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        self.inventory = Inventory.objects.create(
            name="Test Movie",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={"year": 2025, "actors": ["Actor A"]},
        )

    def test_list_tags_for_order_returns_associated_tags(self):
        order = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-04-01",
            embargo_date="2026-04-30",
            is_active=True,
        )
        tag1 = OrderTag.objects.create(name="Priority", is_active=True)
        tag2 = OrderTag.objects.create(name="Urgent", is_active=True)
        order.tags.set([tag1, tag2])

        response = self.client.get(f"/orders/{order.id}/tags/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        returned_names = {tag["name"] for tag in response.data}
        self.assertEqual(returned_names, {"Priority", "Urgent"})

    def test_list_tags_for_order_returns_empty_list_when_no_tags(self):
        order = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-05-01",
            embargo_date="2026-05-31",
            is_active=True,
        )

        response = self.client.get(f"/orders/{order.id}/tags/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
