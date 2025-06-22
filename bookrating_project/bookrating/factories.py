
import factory
from bookrating.models import Work

print("FACTORY LOADED")

class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Work

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker("sentence", nb_words=4)
    original_year = 2000
    avg_rating = 4.2
    ratings_count = 500
