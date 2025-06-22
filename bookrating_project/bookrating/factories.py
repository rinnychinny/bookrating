
import factory
from bookrating.models import Work, Author

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
