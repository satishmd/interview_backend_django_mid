from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order, OrderTag


class OrdersByTagTestCase(TestCase):
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

    def test_list_orders_for_tag_returns_associated_orders(self):
        tag = OrderTag.objects.create(name="Priority", is_active=True)

        order1 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-04-01",
            embargo_date="2026-04-30",
            is_active=True,
        )
        order2 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-05-01",
            embargo_date="2026-05-31",
            is_active=True,
        )
        order1.tags.add(tag)
        order2.tags.add(tag)

        response = self.client.get(f"/orders/tags/{tag.id}/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        returned_order_ids = {order["id"] for order in response.data}
        self.assertEqual(returned_order_ids, {order1.id, order2.id})

    def test_list_orders_for_tag_returns_empty_list_when_unused(self):
        tag = OrderTag.objects.create(name="Unused", is_active=True)

        response = self.client.get(f"/orders/tags/{tag.id}/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
