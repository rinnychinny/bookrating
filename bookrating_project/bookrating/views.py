# Main landing view that demonstrates API calls as URLs

import sys
import platform
import django
import pkg_resources
from django.contrib.auth import get_user_model
from django.conf import settings


from django.http import HttpResponse
from django.urls import reverse, NoReverseMatch
from bookrating.models import Work, Author


def safe_reverse(viewname, *args, **kwargs):
    # helper function to get url from viewname with args
    try:
        return reverse(viewname, *args, **kwargs)
    except NoReverseMatch:
        return None


def api_index(request):
    # main landing page view

    html = "<h1>API Example Endpoints</h1>"

    # helper function to display text and url of link
    def render_links(link_defs):
        html = ""
        for desc, viewname, args, query in link_defs:
            url = safe_reverse(viewname, args=args)
            if url:
                if query:
                    url += f"?{query}"
            html += f"<li>{desc}: <a href='{url}'>{url}</a></li>"
        return html

    # API root
    html += "<h2>API Root</h2><ul>"
    api_link = [("API Root", "api-root", [], "")]
    html += render_links(api_link)
    html += "</ul>"

    # List endpoints
    html += "<h2>API List Endpoints</h2><ul>"
    list_links = [
        ("All Works", "work-list", [], ""),
        ("All Authors", "author-list", [], ""),
        ("All Editions", "edition-list", [], ""),
        ("All Work-Author Links", "workauthor-list", [], ""),
        ("All Edition Ratings", "rating-list", [], ""),
    ]
    html += render_links(list_links)
    html += "</ul>"

    # Detail/custom endpoints
    html += "<h2>Example Detail & Custom Endpoints</h2><ul>"
    work = Work.objects.first()
    author = Author.objects.first()

    if work:
        work_links = [
            ("Work Detail", "work-detail", [work.pk], ""),
            ("Work Editions", "work-editions", [work.pk], ""),
            ("Work Also Loved", "work-also-loved", [work.pk], ""),
            ("Work Ratings", "work-ratings", [work.pk], ""),
            ("Top Works By Author Contains",
             "work-top-rated-by-author", [], "min_rating=4&author=rowl")
        ]
        html += render_links(work_links)

    if author:
        author_links = [
            ("Author Detail", "author-detail", [author.pk], ""),
            ("Author's Works", "author-works", [author.pk], ""),
        ]
        html += render_links(author_links)

    html += "</ul>"

    # Metadata Section
    html += "<h2>Project Metadata</h2><ul>"
    html += f"<li>Python version: {platform.python_version()}</li>"
    html += f"<li>Django version: {django.get_version()}</li>"
    html += f"<li>OS: {platform.system()} {platform.release()}</li>"

    # Admin info (dummy text unless you're creating a default superuser)
    html += f"<li>Admin credentials: user: admin, password: admin</li>"

    import sys
    import pkgutil

    def get_imported_packages():
        # Collect top-level imported modules
        imported = {name.split('.')[0] for name in sys.modules.keys()}

        # Get names of installed top-level modules
        installed = {module.name for module in pkgutil.iter_modules()}

        # Intersect and sort
        used = sorted(imported & installed)

        return used

    # Show installed packages
    html += "<h2>Imported Packages (Approx)</h2><ul>"
    for pkg in get_imported_packages():
        html += f"<li>{pkg}</li>"
    html += "</ul>"

    return HttpResponse(html)
