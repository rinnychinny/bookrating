#Main landing view that demonstrates API calls as URLs

from django.http import HttpResponse
from django.urls import reverse, NoReverseMatch
from django.utils.html import escape
from bookrating.models import Author, Work


def api_index(request):
    """
    Landing page that shows:
      • api page
      • core api list endpoints
      • a few sample 'works-by-author' links
      • a few sample 'also-loved' links
    """
    
    # helper (don’t crash if a route is missing)
    def safe_reverse(v, *args):
        try:
            return reverse(v, *args)
        except NoReverseMatch:
            return None
    
    # -------------------------------------------------
    # 1. Top-level list endpoints
    # -------------------------------------------------
    top_links = [
        ("API",                 "api-root"),
        ("Authors list",        "author-list"),
        ("Works list",          "work-list"),
        ("Book Editions list",  "bookedition-list"),
        ("Work-Author list",    "workauthor-list"),
    ]
    top_ul = "".join(
        f'<li>{escape(lbl)}: '
        f'<a href="{escape(url)}">{escape(url)}</a></li>'
        if (url := safe_reverse(route)) else
        f'<li>{escape(lbl)}: (unavailable)</li>'
        for lbl, route in top_links
    )

    # -------------------------------------------------
    # 2. A few sample “works for author” links
    # -------------------------------------------------
    author_li = []
    for author in Author.objects.all()[:5]:        # first 5 authors
        url = reverse("author-works", args=[author.pk])
        author_li.append(
            f'<li><a href="{escape(url)}">'
            f'Works by {escape(author.name)}</a></li>'
        )
    authors_ul = "".join(author_li) or "<li>No authors yet</li>"

    # -------------------------------------------------
    # 3. A few sample “also-loved” links
    # -------------------------------------------------
    loved_li = []
    for work in Work.objects.order_by("-ratings_count")[:5]:
        url = reverse("work-also-loved", args=[work.pk])
        loved_li.append(
            f'<li><a href="{escape(url)}">'
            f'People who loved <em>{escape(work.title)}</em> also loved…</a></li>'
        )
    loved_ul = "".join(loved_li) or "<li>No works yet</li>"

    # -------------------------------------------------
    html = f"""
    <html>
      <head>
        <title>BookRating API index</title>
        <style>
          body {{ font-family: Arial; margin: 2rem; }}
          h2  {{ margin-top: 2rem; }}
          li  {{ margin-bottom: .4rem; }}
        </style>
      </head>
      <body>
        <h1>BookRating API – landing page</h1>

        <h2>Top-level endpoints</h2>
        <ul>{top_ul}</ul>

        <h2>Works for sample authors</h2>
        <ul>{authors_ul}</ul>

        <h2>“Also loved” recommendations</h2>
        <ul>{loved_ul}</ul>
      </body>
    </html>
    """
    return HttpResponse(html)


# helper so we don’t crash if a view-name is missing
def _url_exists(viewname):
    try:
        reverse(viewname)
        return True
    except NoReverseMatch:
        return False


