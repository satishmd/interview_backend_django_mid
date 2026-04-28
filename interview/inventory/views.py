from datetime import datetime

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)
from interview.inventory.schemas import InventoryMetaData
from interview.inventory.serializers import (
    InventoryLanguageSerializer,
    InventorySerializer,
    InventoryTagSerializer,
    InventoryTypeSerializer,
)


class InventoryListCreateView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            metadata = InventoryMetaData(**request.data["metadata"])
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        request.data["metadata"] = metadata.dict()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        offset, limit = self.get_pagination_params(request)
        created_after = request.query_params.get("created_after")

        if created_after:
            try:
                parsed_date = self.parse_created_after(created_after)
            except ValueError as exc:
                return Response({"error": str(exc)}, status=400)

            queryset = queryset.filter(created_at__gt=parsed_date)
        
        paginated_queryset = queryset[offset : offset + limit]
        serializer = self.serializer_class(paginated_queryset, many=True)

        return Response(
            {
                "count": queryset.count(),
                "offset": offset,
                "limit": limit,
                "results": serializer.data,
            },
            status=200,
        )

    def get_pagination_params(self, request: Request) -> tuple[int, int]:
        offset = request.query_params.get("offset", 0)
        limit = request.query_params.get("limit", 3)

        try:
            offset = int(offset)
        except (TypeError, ValueError):
            offset = 0

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 3

        if offset < 0:
            offset = 0
        if limit <= 0:
            limit = 3

        return offset, min(limit, 100)

    def get_queryset(self):
        return self.queryset.all()

    @staticmethod
    def parse_created_after(value: str) -> datetime:
        value = value.strip()

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "created_after must be ISO 8601 format, e.g. 2026-04-27 or 2026-04-27T15:00:00"
            )




class InventoryRetrieveUpdateDestroyView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTagListCreateView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTagRetrieveUpdateDestroyView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory_tag)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(
            inventory_tag, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        inventory_tag.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryLanguageListCreateView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryLanguageRetrieveUpdateDestroyView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTypeListCreateView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTypeRetrieveUpdateDestroyView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
