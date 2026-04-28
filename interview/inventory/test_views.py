from datetime import datetime, timedelta
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)


class InventoryListCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/inventory/"

        # Create test data
        self.inventory_type = InventoryType.objects.create(name="Movie")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        self.tag1 = InventoryTag.objects.create(name="Sci-Fi", is_active=True)
        self.tag2 = InventoryTag.objects.create(name="Thriller", is_active=True)

    def test_create_inventory_success(self):
        """Test successful inventory creation"""
        payload = {
            "name": "Inception",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id, self.tag2.id],
            "metadata": {
                "year": 2010,
                "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
                "imdb_rating": Decimal("8.8"),
                "rotten_tomatoes_rating": 87,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Inception")
        self.assertEqual(response.data["type"], self.inventory_type.id)
        self.assertEqual(Inventory.objects.count(), 1)

    def test_create_inventory_missing_metadata(self):
        """Test inventory creation fails when metadata is missing"""
        payload = {
            "name": "Inception",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id],
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("metadata", str(response.data))

    def test_create_inventory_invalid_metadata_missing_fields(self):
        """Test inventory creation fails when metadata is missing required fields"""
        payload = {
            "name": "Inception",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id],
            "metadata": {
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                # Missing imdb_rating and rotten_tomatoes_rating
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_create_inventory_invalid_metadata_wrong_types(self):
        """Test inventory creation fails when metadata has wrong types"""
        payload = {
            "name": "Inception",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id],
            "metadata": {
                "year": "jshfdh",  # Should be int
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_create_inventory_missing_name(self):
        """Test inventory creation fails when name is missing"""
        payload = {
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id],
            "metadata": {
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_create_inventory_invalid_type_id(self):
        """Test inventory creation fails with invalid type ID"""
        payload = {
            "name": "Inception",
            "type": 9999,  # Non-existent ID
            "language": self.inventory_language.id,
            "tags": [self.tag1.id],
            "metadata": {
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_list_all_inventory(self):
        """Test listing all inventory items"""
        # Create test inventory items
        inventory1 = Inventory.objects.create(
            name="Inception",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        )
        inventory1.tags.add(self.tag1)

        inventory2 = Inventory.objects.create(
            name="The Matrix",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 1999,
                "actors": ["Keanu Reeves"],
                "imdb_rating": 8.7,
                "rotten_tomatoes_rating": 88,
            },
        )
        inventory2.tags.add(self.tag2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_inventory_with_created_after_filter(self):
        """Test filtering inventory by created_after date"""
        # Create first inventory with old timestamp
        inventory1 = Inventory.objects.create(
            name="Inception",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        )
        inventory1.created_at = datetime.now() - timedelta(days=1)
        inventory1.save()

        # Create second inventory with current timestamp
        inventory2 = Inventory.objects.create(
            name="The Matrix",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 1999,
                "actors": ["Keanu Reeves"],
                "imdb_rating": 8.7,
                "rotten_tomatoes_rating": 88,
            },
        )

        # Filter by a date after inventory1 but before inventory2
        filter_date = inventory1.created_at + timedelta(seconds=1)
        response = self.client.get(
            self.url,
            {"created_after": filter_date.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], "The Matrix")

    def test_list_inventory_with_invalid_created_after_format(self):
        """Test filtering with invalid ISO 8601 format raises error"""
        response = self.client.get(
            self.url,
            {"created_after": "2026/04/27"},  # Invalid format
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertIn("ISO 8601 format", response.data["error"])

    def test_list_inventory_with_empty_created_after(self):
        """Test filtering with empty created_after value"""
        response = self.client.get(
            self.url,
            {"created_after": "   "},  # Whitespace only
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_list_inventory_with_date_only_created_after(self):
        """Test filtering with ISO 8601 date-only format"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        inventory = Inventory.objects.create(
            name="Inception",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        )

        response = self.client.get(
            self.url,
            {"created_after": str(yesterday)},  # Date only
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["name"], "Inception")

    def test_list_inventory_with_future_created_after_returns_empty(self):
        """Test filtering with future date returns no results"""
        Inventory.objects.create(
            name="Inception",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={
                "year": 2010,
                "actors": ["Leonardo DiCaprio"],
                "imdb_rating": 8.8,
                "rotten_tomatoes_rating": 87,
            },
        )

        future_date = datetime.now() + timedelta(days=1)
        response = self.client.get(
            self.url,
            {"created_after": future_date.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_create_inventory_with_multiple_tags(self):
        """Test creating inventory with multiple tags"""
        tag3 = InventoryTag.objects.create(name="Action", is_active=True)

        payload = {
            "name": "Mission Impossible",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [self.tag1.id, self.tag2.id, tag3.id],
            "metadata": {
                "year": 2023,
                "actors": ["Tom Cruise"],
                "imdb_rating": 7.8,
                "rotten_tomatoes_rating": 82,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["tags"]), 3)

    def test_create_inventory_with_no_tags(self):
        """Test creating inventory with empty tags list"""
        payload = {
            "name": "Test Movie",
            "type": self.inventory_type.id,
            "language": self.inventory_language.id,
            "tags": [],
            "metadata": {
                "year": 2020,
                "actors": ["Actor Name"],
                "imdb_rating": 7.5,
                "rotten_tomatoes_rating": 80,
            },
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["tags"]), 0)
