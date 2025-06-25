from django.db import models

# Work id corresponds to goodbooks work_id
# work_id refers to the book (regardless of edition/version)


class Work(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(
        "Author", through="WorkAuthor", related_name="works")
    original_year = models.IntegerField(null=True, blank=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2)
    ratings_count = models.PositiveIntegerField()

# BookEdition id corresponds to book_id in goodbooks
# Book edition holds data for each separate version of a book


class BookEdition(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.ForeignKey(Work, on_delete=models.CASCADE,
                             related_name="editions")
    isbn = models.CharField(max_length=13, null=True, blank=True)
    isbn13 = models.CharField(max_length=13, null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    # Edition-specific popularity
    ratings_count = models.PositiveIntegerField()
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2)

# Joins works to authors


class WorkAuthor(models.Model):
    work = models.ForeignKey(Work,   on_delete=models.CASCADE)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "author"], name="unique_work_author")
        ]

# Table of distinct authors


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Rating(models.Model):
    user_id = models.IntegerField()
    edition = models.ForeignKey(BookEdition, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
