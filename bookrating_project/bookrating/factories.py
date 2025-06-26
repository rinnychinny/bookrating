
import factory
from bookrating.models import Work, Author, BookEdition


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Work

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker("sentence", nb_words=4)
    original_year = 2000
    avg_rating = 4.2
    ratings_count = 500


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name")


class BookEditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookEdition
    id = factory.Sequence(lambda n: n + 1000)
    work = factory.SubFactory(WorkFactory)
    isbn = factory.Faker("isbn13")
    isbn13 = factory.Faker("isbn13")
    language_code = "en"
    avg_rating = 4.0
    ratings_count = 100
