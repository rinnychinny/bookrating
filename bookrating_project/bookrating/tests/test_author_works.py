from rest_framework.test import APITestCase
from django.urls import reverse

from bookrating.factories import AuthorFactory, WorkFactory
from bookrating.models import Work

class AuthorWorksAPITest(APITestCase):
    def setUp(self):
        # One author with two works
        self.author = AuthorFactory()
        self.work1  = WorkFactory()
        self.work2  = WorkFactory()
        self.work1.authors.add(self.author)
        self.work2.authors.add(self.author)

        # A second author with just one work (different author to the above)
        self.other_author = AuthorFactory()
        self.other_work   = WorkFactory()
        self.other_work.authors.add(self.other_author)

    #test GET on one author with multiple works
    def test_author_works_endpoint_lists_only_this_authors_works(self):
        url = reverse("author-works", kwargs={"pk": self.author.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Response should contain exactly the two works linked to self.author
        titles = {w["title"] for w in resp.data}
        self.assertSetEqual(titles, {self.work1.title, self.work2.title})

    #test GET on invalid author returns a 404
    def test_invalid_author_returns_404(self):
        url = reverse("author-works", kwargs={"pk": 99999})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    #test GET on author returns a hyperlink to a list of works
    def test_author_list_contains_hyperlink_to_works(self):
        url = reverse("author-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Find the entry for self.author
        results = resp.data.get("results", resp.data)  # fall back if not paginated
        author_item = next(a for a in results if a["id"] == self.author.id)
        self.assertIn("works", author_item)
        self.assertTrue(author_item["works"].endswith(f"/authors/{self.author.id}/works/"))
