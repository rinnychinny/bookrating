from rest_framework import serializers
from .models import Work, Author, BookEdition, WorkAuthor, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "edition", "rating"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    works = serializers.HyperlinkedIdentityField(
        view_name='author-works',
        lookup_field='pk'
    )

    class Meta:
        model = Author
        fields = ["id", "name", "works"]


class WorkListSerializer(serializers.HyperlinkedModelSerializer):
    # Get DRF to add a hyperlink to the work detail view
    url = serializers.HyperlinkedIdentityField(
        view_name="work-detail",
        lookup_field="pk",
    )

    class Meta:
        model = Work
        fields = "__all__"


class BookEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEdition
        fields = "__all__"


class WorkDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    editions = BookEditionSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = ["id", "title", "original_year", "avg_rating",
                  "ratings_count", "authors", "editions"]


class WorkWithFanCountSerializer(serializers.ModelSerializer):
    five_star_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Work
        fields = ["id", "title", "avg_rating", "five_star_count"]


class WorkAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkAuthor
        fields = ["id", "work", "author"]
