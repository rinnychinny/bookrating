from bookrating.models import (
    Work, BookEdition,
    Author, WorkAuthor,
    Tag, EditionTag,
    Rating,
)
from datetime import datetime
import csv
import os
import sys
from pathlib import Path
import django

sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookrating_project.settings")
django.setup()

# Usage: python loader.py

# Loads books, editions, authors and ratings from
# goodbooks-10k CSVs into a normalised Django database schema.
# Tags excluded due to data restriction


# used in dev .. for adding of data to production remove these deletes!
print("Clearing existing data...")
Rating.objects.all().delete()
WorkAuthor.objects.all().delete()
Author.objects.all().delete()
BookEdition.objects.all().delete()
Work.objects.all().delete()


DATA_DIR = Path(__file__).resolve().parents[2] / "goodbooks-10k"

# change this to  None for a full load - 6mm ratings...
LIMIT_BOOKS = 20        # ← import ONLY the first LIMIT_BOOKS rows of books.csv

# ---------------------------------------------------------------------------
# 1. Works, Editions, Authors   (collect IDs while you loop)
# ---------------------------------------------------------------------------
kept_edition_ids = set()      # store edition IDs we keep
kept_work_ids = set()      # needed later to filter by work


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


# ---------------------------------------------------------------------------
# 1. Works, Editions, Authors
# ---------------------------------------------------------------------------
with (DATA_DIR / "books.csv").open(encoding="utf-8") as fp:
    reader = csv.DictReader(fp)
    # reader.fieldnames = [fn.strip() for fn in reader.fieldnames] #clean up leading spaces on some field names
    for i, row in enumerate(reader, start=1):
        if LIMIT_BOOKS and i > LIMIT_BOOKS:
            break           # Work

        book_id = int(row["book_id"])
        work_id = int(row["work_id"])
        kept_edition_ids.add(book_id)
        kept_work_ids.add(work_id)

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

print("Books & authors loaded.")

BATCH, BATCH_SIZE = [], 5_000


def flush_batch():
    if BATCH:
        Rating.objects.bulk_create(BATCH)
        BATCH.clear()


with (DATA_DIR / "ratings.csv").open(encoding="utf-8") as fp:
    for row in csv.DictReader(fp):
        edition_id = int(row["book_id"])
        if edition_id not in kept_edition_ids:
            continue                     # skip ratings outside subset
        BATCH.append(
            Rating(
                user_id=int(row["user_id"]),
                edition_id=edition_id,
                rating=int(row["rating"]),
            )
        )
        if len(BATCH) >= BATCH_SIZE:
            flush_batch()
flush_batch()

print("Ratings loaded.")
print("Done!")
