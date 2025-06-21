from rest_framework import viewsets
from .models import Work, Author, BookEdition
from .serializers import WorkListSerializer, WorkDetailSerializer, AuthorSerializer, BookEditionSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = (Work.objects.all()
                .prefetch_related("authors", "editions"))

    def get_serializer_class(self):
        if self.action == "list":
            return WorkListSerializer #/api/works returns list
        return WorkDetailSerializer   #/api/works/<id> returns single work detail

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookEditionViewSet(viewsets.ModelViewSet):
    queryset = BookEdition.objects.all()
    serializer_class = BookEditionSerializer
