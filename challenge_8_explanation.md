# Create Inventory Item

## Goal
Add a new inventory item through the API with metadata containing these fields:
- `year`
- `actors`
- `imdb_rating`
- `rotten_tomatoes_rating`
- `film_locations`

## What you're solving
The Inventory API needs to accept a POST request that creates a new `Inventory` record. The `metadata` field is stored as JSON, so the request body must include those fields inside `metadata`.

## How the API works in this project
1. The inventory endpoint is registered under `/inventory/`.
2. `InventoryListCreateView` handles GET and POST requests for inventory items.
3. The `InventorySerializer` returns the inventory data with nested type, language, and tags.
4. `InventoryMetaData` validates the metadata structure before saving.

## What you need to do
### 1. Create supporting records first
Before you create an inventory item, add the required supporting records:
- `InventoryType` for the item category
    - POST `/inventory/types/` with:

        ```json
        {
        "name": "Movie"
        }
        ```
- `InventoryLanguage` for the item language
    - POST `/inventory/languages/` with:

        ```json
        {
        "name": "English"
        }
        ```


- `InventoryTag` records if you want to tag the film
    - POST `/inventory/tags/` with:

        ```json
        {
        "name": "Sci-Fi",
        "is_active": true
        }
        ```


The inventory item requires valid `type` and `language` IDs.

### 2. Create the inventory item
Once the supporting records exist, send a POST to `/inventory/` with this JSON body:

```json
{
  "name": "Inception",
  "type": 1,
  "language": 1,
  "tags": [1],
  "metadata": {
    "year": 2010,
    "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt"],
    "imdb_rating": 8.8,
    "rotten_tomatoes_rating": 87,
    "film_locations": ["Los Angeles", "Paris", "Tokyo"]
  }
}
```

#### Why this works
- `name`, `type`, and `language` are required fields on the `Inventory` model.
- `tags` is a many-to-many relation and may be sent as an empty list.
- `metadata` is a JSON field that stores all the extra movie details.
- The API view validates `metadata` using `InventoryMetaData`, then creates the inventory item using DRF serialization.

#### Troubleshooting common issues
- `type` or `language` is invalid: check that the referenced IDs exist.
- `metadata` fields are missing: make sure the JSON includes each required field.
- Bad field names: use exactly `year`, `actors`, `imdb_rating`, `rotten_tomatoes_rating`, and `film_locations`.
- If you get a 400 response, inspect the response body for serializer or validation errors.

### 3. Confirm the item was created
Use below GET calls and check that your new item appears in the returned `results` list.

- List all inventory items:
  - `GET /inventory/`

- Get items created after a specific date:
  - `GET /inventory/?created_after=2026-04-01`

- Use pagination with `offset` and `limit`:
  - `GET /inventory/?offset=0&limit=3`
  - `GET /inventory/?offset=3&limit=3`

- Combine filtering and pagination:
  - `GET /inventory/?created_after=2026-04-01&offset=0&limit=3`

