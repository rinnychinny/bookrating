from rest_framework import viewsets
from .models import Work
from .serializers import WorkSerializer

class WorkViewSet(viewsets.ReadOnlyModelViewSet):   # Read-only
    """
    GET /api/works/        → list (paginated)
    GET /api/works/<id>/   → single work
    """
    queryset = Work.objects.all().prefetch_related("authors", "editions")
    serializer_class = WorkSerializer
