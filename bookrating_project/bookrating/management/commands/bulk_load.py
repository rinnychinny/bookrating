import csv
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from bookrating.models import Work, BookEdition, Author, Rating, WorkAuthor


def parse_date(s: str | None):
    """Convert MM/DD/YYYY to datetime.date, or None."""
    if not s:
        return None
    try:
        return datetime.strptime(s, "%m/%d/%Y").date()
    except ValueError:
        return None


def _parse_year(s):
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


class Command(BaseCommand):
    help = "Bulk load book and ratings data from CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--books", type=str, help="Path to book data CSV", default=None
        )
        parser.add_argument(
            "--ratings", type=str, help="Path to ratings data CSV", default=None
        )

    def handle(self, *args, **options):
        books_path = options["books"]
        ratings_path = options["ratings"]

        if not books_path and not ratings_path:
            raise CommandError(
                "You must provide at least one of --books or --ratings")

        if books_path:
            path = Path(books_path)
            if not path.exists():
                raise CommandError(f"Books file not found: {path}")
            self.stdout.write(f"Loading books from: {path}")
            self.load_books(path)

        if ratings_path:
            path = Path(ratings_path)
            if not path.exists():
                raise CommandError(f"Ratings file not found: {path}")
            self.stdout.write(f"Loading ratings from: {path}")
            self.load_ratings(path)

        self.stdout.write(self.style.SUCCESS("Bulk loading completed."))

    def load_books(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):

                # Work
                work, _ = Work.objects.get_or_create(
                    id=int(row["work_id"]),
                    defaults={
                        "title": (row["original_title"] or row["title"]).strip(),
                        "original_year": _parse_year(row["original_publication_year"]),
                        "avg_rating": float(row["average_rating"] or 0),
                        "ratings_count": int(row["work_ratings_count"] or 0),
                    },
                )

                # Edition
                BookEdition.objects.get_or_create(
                    id=int(row["book_id"]),
                    defaults={
                        "work": work,
                        "isbn": row["isbn"] or None,
                        "isbn13": row["isbn13"] or None,
                        "language_code": row["language_code"] or None,
                        "ratings_count": int(row["ratings_count"] or 0),
                        "avg_rating": float(row["average_rating"] or 0),
                    },
                )

                # Authors
                for name in (n.strip() for n in row["authors"].split(",")):
                    if not name:
                        continue
                    author, _ = Author.objects.get_or_create(name=name)
                    work.authors.add(author)
                    # also add into WorkAuthor junction table
                    WorkAuthor.objects.get_or_create(work=work, author=author)

    def load_ratings(self, path):
        BATCH, BATCH_SIZE = [], 5_000
        seen_pairs = set()
        skipped_duplicates = 0

        def flush_batch():
            if BATCH:
                try:
                    # ignore_conflicts to silently skip existing duplicates in the db
                    Rating.objects.bulk_create(BATCH, ignore_conflicts=True)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(
                        f"Batch insert failed: {e}"))
            BATCH.clear()

        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                user_id = int(row["user_id"])
                edition_id = int(row["book_id"])
                key = (user_id, edition_id)

                if key in seen_pairs:
                    skipped_duplicates += 1
                    continue

                seen_pairs.add(key)
                BATCH.append(
                    Rating(
                        user_id=user_id,
                        edition_id=edition_id,
                        rating=int(row["rating"]),
                    )
                )
                if len(BATCH) >= BATCH_SIZE:
                    flush_batch()
        flush_batch()
        self.stdout.write(
            f"Skipped {skipped_duplicates} duplicate ratings in input file.")
