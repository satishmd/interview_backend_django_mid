from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryType,
)
from interview.order.models import Order


class OrderListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/orders/"

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

    def test_list_all_orders(self):
        """Test listing all orders without filters"""
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
            is_active=False,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        order_ids = [order["id"] for order in response.data]
        self.assertIn(order1.id, order_ids)
        self.assertIn(order2.id, order_ids)

    def test_list_orders_filtered_by_date_range(self):
        """Test filtering orders by start_date and embargo_date"""
        order1 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-04-01",
            embargo_date="2026-04-30",
            is_active=True,
        )
        order2 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-05-01",
            embargo_date="2026-05-15",
            is_active=True,
        )
        order3 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-06-01",
            embargo_date="2026-06-30",
            is_active=True,
        )

        # Filter for orders between 2026-04-15 and 2026-05-31
        response = self.client.get(
            self.url,
            {"start_date": "2026-04-15", "embargo_date": "2026-05-31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], order2.id)

    def test_list_orders_filtered_by_date_range_multiple_results(self):
        """Test filtering orders by date range with multiple results"""
        order1 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-04-01",
            embargo_date="2026-04-30",
            is_active=True,
        )
        order2 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-05-01",
            embargo_date="2026-05-15",
            is_active=True,
        )
        order3 = Order.objects.create(
            inventory=self.inventory,
            start_date="2026-05-16",
            embargo_date="2026-05-31",
            is_active=True,
        )

        # Filter for orders between 2026-04-01 and 2026-05-31
        response = self.client.get(
            self.url,
            {"start_date": "2026-04-01", "embargo_date": "2026-05-31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        order_ids = [order["id"] for order in response.data]
        self.assertIn(order1.id, order_ids)
        self.assertIn(order2.id, order_ids)
        self.assertIn(order3.id, order_ids)

    def test_list_orders_filtered_by_date_range_no_results(self):
        """Test filtering orders by date range with no results"""
        Order.objects.create(
            inventory=self.inventory,
            start_date="2026-06-01",
            embargo_date="2026-06-30",
            is_active=True,
        )

        # Filter for orders in April
        response = self.client.get(
            self.url,
            {"start_date": "2026-04-01", "embargo_date": "2026-04-30"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_orders_filtered_invalid_date_format(self):
        """Test filtering with invalid date format returns 400"""
        response = self.client.get(
            self.url,
            {"start_date": "2026/04/15", "embargo_date": "2026-05-15"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_list_orders_filtered_start_date_after_embargo_date(self):
        """Test filtering with start_date after embargo_date returns 400"""
        response = self.client.get(
            self.url,
            {"start_date": "2026-05-15", "embargo_date": "2026-04-15"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn("start_date cannot be after embargo_date", response.data["error"])