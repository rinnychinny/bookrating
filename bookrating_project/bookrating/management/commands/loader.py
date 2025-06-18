# Usage:
#   $ python manage.py shell < load_goodbooks_simple.py
#
# This loads books, editions, authors, tags, and ratings from
# goodbooks-10k CSVs into a normalised Django database schema.

import csv
from datetime import datetime
from pathlib import Path

from bookrating.models import (
    Work, BookEdition,
    Author, WorkAuthor,
    Tag, EditionTag,
    Rating,
)

DATA_DIR = Path("..") / "goodbooks-10k"

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
    #reader.fieldnames = [fn.strip() for fn in reader.fieldnames] #clean up leading spaces on some field names
    for row in reader:
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
            #also add into WorkAuthor junction table
            WorkAuthor.objects.get_or_create(work=work, author=author)

print("Books & authors loaded.")


# ---------------------------------------------------------------------------
# 2. Tags
# ---------------------------------------------------------------------------
with (DATA_DIR / "tags.csv").open(encoding="utf-8") as fp:
    for row in csv.DictReader(fp):
        Tag.objects.get_or_create(
            id=int(row["tag_id"]),
            defaults={"name": row["tag_name"].strip()},
        )

with (DATA_DIR / "book_tags.csv").open(encoding="utf-8") as fp:
    for row in csv.DictReader(fp):
        EditionTag.objects.get_or_create(
            edition_id=int(row["goodreads_book_id"]),
            tag_id=int(row["tag_id"]),
            defaults={"count": int(row["count"])},
        )

print("Tags loaded.")


# ---------------------------------------------------------------------------
# 3. Ratings (insert in batches to avoid memory issues)
# ---------------------------------------------------------------------------
BATCH, BATCH_SIZE = [], 5_000

def flush_batch():
    if BATCH:
        Rating.objects.bulk_create(BATCH)
        BATCH.clear()

with (DATA_DIR / "ratings.csv").open(encoding="utf-8") as fp:
    for row in csv.DictReader(fp):
        BATCH.append(
            Rating(
                user_id=int(row["user_id"]),
                edition_id=int(row["book_id"]),
                rating=int(row["rating"]),
            )
        )
        if len(BATCH) >= BATCH_SIZE:
            flush_batch()
flush_batch()

print("Ratings loaded.")
print("Done!")
