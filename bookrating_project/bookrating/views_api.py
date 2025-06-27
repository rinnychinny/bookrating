from django.db.models import Case, When, IntegerField, Value, Count, Avg

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (Work,
                     Author,
                     BookEdition,
                     Rating,
                     WorkAuthor)

from .serializers import (WorkListSerializer,
                          WorkDetailSerializer,
                          AuthorSerializer,
                          BookEditionSerializer,
                          WorkWithFanCountSerializer,
                          WorkAuthorSerializer,
                          RatingSerializer)


class WorkViewSet(viewsets.ModelViewSet):
    queryset = (Work.objects.all()
                .prefetch_related("authors", "editions"))

    def get_serializer_class(self):
        if self.action == "list":
            return WorkListSerializer  # /api/works returns list
        return WorkDetailSerializer  # /api/works/<id> returns single work detail

    @action(detail=False, methods=["get"])
    def top_rated_by_author(self, request):
        author_query = request.query_params.get("author", "")
        min_rating = float(request.query_params.get("min_rating", 4.0))

        works = Work.objects.filter(
            avg_rating__gt=min_rating,
            authors__name__icontains=author_query
        ).order_by("-avg_rating").distinct()

        serializer = self.get_serializer(works, many=True)
        return Response(serializer.data)

    # custom endpoint to show ratings info (bucket counts, average, total acount) for all editions of one work

    @action(detail=True, methods=["get"])
    def ratings(self, request, pk=None):
        work = self.get_object()
        # get all ratings for any edition of this work
        ratings_qs = (
            Rating.objects
            .filter(edition__work=work)
            .values_list("rating")
        )
        # Get average and total count
        summary = ratings_qs.aggregate(
            avg_rating=Avg("rating"),
            total_ratings=Count("rating")
        )
        # Group by each rating value
        buckets = (
            ratings_qs.values("rating")
            .annotate(count=Count("id"))
            .order_by("rating")
        )

        # Format the bucket counts as a dict
        distribution = {b["rating"]: b["count"] for b in buckets}

        return Response({
            "sample_average_rating": round(summary["avg_rating"], 2) if summary["avg_rating"] else None,
            "sample_total_ratings": summary["total_ratings"],
            "distribution": distribution
        })

    # add custom endpoint to show all editions for one work
    @action(detail=True, methods=["get"])
    def editions(self, request, pk=None):
        work = self.get_object()
        editions = work.editions.all()
        serializer = BookEditionSerializer(
            editions, many=True, context={"request": request})
        return Response(serializer.data)

    # Custom endpoint for 'also-loved'
    @action(detail=True, methods=["get"])
    def also_loved(self, request, pk=None):
        """
        Works whose editions received 5-star ratings from users
        who also gave this Work a 5-star rating, ranked by avg_rating, count.
        """
        target_work = self.get_object()

        # users who rated ANY edition of this work with 5
        fan_user_ids = (
            Rating.objects
            .filter(edition__work=target_work, rating=5)
            .values_list("user_id", flat=True)
        )

        # 5-star ratings by those users on OTHER works
        related_5s = (
            Rating.objects
            .filter(user_id__in=fan_user_ids, rating=5)
            .exclude(edition__work=target_work)
        )

        # group by work and count DISTINCT users
        work_counts = (
            related_5s
            .values("edition__work")
            .annotate(five_star_count=Count("user_id", distinct=True))
            .order_by("-five_star_count")
        )

        # fetch Work objects & attach the count
        id_to_count = {w["edition__work"]: w["five_star_count"]
                       for w in work_counts}

        # annotate using a CASE expression (for static dict -> queryset mapping)
        whens = [When(id=wid, then=Value(count))
                 for wid, count in id_to_count.items()]
        works = (
            Work.objects
            .filter(id__in=id_to_count.keys())
            .annotate(five_star_count=Case(*whens, output_field=IntegerField()))
            .order_by("-five_star_count")
        )

        # final ordering by avg_rating, then five_Star_count
        data = WorkWithFanCountSerializer(
            works.order_by("-avg_rating", "-five_star_count"), many=True
        ).data
        return Response(data)


class AuthorViewSet(viewsets.ModelViewSet):
    # use order_by to prevent pagination warning in tests
    queryset = Author.objects.all().order_by("id")
    serializer_class = AuthorSerializer
    # create custom endpoint to show all works of a particular author

    @action(detail=True, methods=["get"])
    def works(self, request, pk=None):
        author = self.get_object()
        # order by rating descending so that favourite works appear first
        works = author.works.all().prefetch_related(
            "authors", "editions").order_by("-avg_rating")
        serializer = WorkListSerializer(
            works, many=True, context={"request": request})
        return Response(serializer.data)


class BookEditionViewSet(viewsets.ModelViewSet):
    queryset = BookEdition.objects.all()
    serializer_class = BookEditionSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class WorkAuthorViewSet(viewsets.ModelViewSet):
    # use order_by to prevent pagination warning in tests
    queryset = WorkAuthor.objects.all().order_by("id")
    serializer_class = WorkAuthorSerializer
