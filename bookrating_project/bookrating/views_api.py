from django.db.models import Case, When, IntegerField, Value, Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Work, Author, BookEdition, Rating
from .serializers import   (WorkListSerializer, 
                            WorkDetailSerializer,
                            AuthorSerializer,
                            BookEditionSerializer,
                            WorkWithFanCountSerializer)

class WorkViewSet(viewsets.ModelViewSet):
    queryset = (Work.objects.all()
                .prefetch_related("authors", "editions"))

    def get_serializer_class(self):
        if self.action == "list":
            return WorkListSerializer #/api/works returns list
        return WorkDetailSerializer   #/api/works/<id> returns single work detail
    
    # Custom endpoint for 'also-loved'
    @action(detail=True, methods=["get"])
    def also_loved(self, request, pk=None):
        """
        Works whose editions received 5-star ratings from users
        who also gave this Work a 5-star rating, ranked by count.
        """
        target_work = self.get_object()

        #users who rated ANY edition of this work with 5
        fan_user_ids = (
            Rating.objects
            .filter(edition__work=target_work, rating=5)
            .values_list("user_id", flat=True)
        )

        #5-star ratings by those users on OTHER works
        related_5s = (
            Rating.objects
            .filter(user_id__in=fan_user_ids, rating=5)
            .exclude(edition__work=target_work)
        )

        #group by work and count DISTINCT users
        work_counts = (
            related_5s
            .values("edition__work")
            .annotate(five_star_count=Count("user_id", distinct=True))
            .order_by("-five_star_count")
        )

        #fetch Work objects & attach the count

        id_to_count = {w["edition__work"]: w["five_star_count"] for w in work_counts}

        # annotate using a CASE expression (for static dict -> queryset mapping)
        whens = [When(id=wid, then=Value(count)) for wid, count in id_to_count.items()]
        works = (
            Work.objects
            .filter(id__in=id_to_count.keys())
            .annotate(five_star_count=Case(*whens, output_field=IntegerField()))
            .order_by("-five_star_count")
        )

        data = WorkWithFanCountSerializer(
            works.order_by("-five_star_count"), many=True
        ).data
        return Response(data)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookEditionViewSet(viewsets.ModelViewSet):
    queryset = BookEdition.objects.all()
    serializer_class = BookEditionSerializer
