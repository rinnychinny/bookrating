from datetime import datetime
import csv
import os
import django
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookrating_project.settings")
django.setup()

# autopep8: off
from bookrating.models import (
    Work, BookEdition,
    Author, WorkAuthor,
    Rating,
)
# autopep8: on

# Usage: python loader.py

# Loads books, editions, authors and ratings from
# goodbooks-10k CSVs into a normalised Django database schema.
# Tags excluded due to data restriction


# used in dev for creating data from scratch..
# for adding of data use bulk_load command in bulk_load.py
print("Clearing existing data...")
Rating.objects.all().delete()
WorkAuthor.objects.all().delete()
Author.objects.all().delete()
BookEdition.objects.all().delete()
Work.objects.all().delete()


DATA_DIR = Path(__file__).resolve().parents[2] / "goodbooks-10k-filtered"
books_fname = "filtered_books.csv"
ratings_fname = "filtered_ratings.csv"

# change this to  None for a full load, or an integer to limit
# fyi 6mm ratings on unfiltered dataset ...
LIMIT_BOOKS = None   # ← import ONLY the first LIMIT_BOOKS rows of the books csv file

# ---------------------------------------------------------------------------
# 1. Works, Editions, Authors   (collect IDs looping)
# ---------------------------------------------------------------------------
kept_edition_ids = set()      # store edition IDs to keep
# kept_work_ids = set()      # needed later to filter by work


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
# 1. Works, Editions, Authors, WorkAuthor
# ---------------------------------------------------------------------------
with (DATA_DIR / books_fname).open(encoding="utf-8") as fp:
    reader = csv.DictReader(fp)
    for i, row in enumerate(reader, start=1):
        if LIMIT_BOOKS and i > LIMIT_BOOKS:
            break           # Work

        book_id = int(row["book_id"])
        work_id = int(row["work_id"])
        kept_edition_ids.add(book_id)  # needed for filtering ratings
        # kept_work_ids.add(work_id)

        work, _ = Work.objects.get_or_create(
            id=work_id,
            defaults={
                "title": (row["original_title"] or row["title"]).strip(),
                "original_year": _parse_year(row["original_publication_year"]),
                "avg_rating": float(row["average_rating"] or 0),
                "ratings_count": int(row["work_ratings_count"] or 0),
            },
        )

        # Edition
        BookEdition.objects.get_or_create(
            id=book_id,
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

print("Books, authors and editions loaded.")

# ---------------------------------------------------------------------------
# 2. Ratings
# ---------------------------------------------------------------------------

# Batch ratings for speed
BATCH, BATCH_SIZE = [], 5_000


def flush_batch():
    if BATCH:
        Rating.objects.bulk_create(BATCH)
        BATCH.clear()


print("Loading ratings...")

seen_pairs = set()
skipped_duplicates = 0

with (DATA_DIR / ratings_fname).open(encoding="utf-8") as fp:
    for row in csv.DictReader(fp):
        edition_id = int(row["book_id"])
        user_id = int(row["user_id"])
        key = (user_id, edition_id)
        if edition_id not in kept_edition_ids:
            continue                     # skip ratings outside subset
        if key in seen_pairs:
            skipped_duplicates += 1
            continue  # skip duplicates
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

print("Ratings loaded.")
print(f"Skipped {skipped_duplicates:,} duplicate ratings.")
print("Done!")
