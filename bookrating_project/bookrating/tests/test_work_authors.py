from rest_framework.test import APITestCase
from django.urls import reverse

from bookrating.factories import WorkFactory, AuthorFactory
from bookrating.models import WorkAuthor

class WorkAuthorsTest(APITestCase):
    def setUp(self):
        self.author1 = AuthorFactory(name="Author One")
        self.author2 = AuthorFactory(name="Author Two")
        self.author3 = AuthorFactory(name="Author Three")
        #build a work with two authors
        self.work = WorkFactory()
        self.work.authors.set([self.author1, self.author2])

    #test the DB creates two entries in WorkAuthor for this work
    def test_db_relationship(self):
        self.assertEqual(self.work.authors.count(), 2)
        self.assertEqual(
            WorkAuthor.objects.filter(work=self.work).count(),
            2
        )

    #test the GET on work detail returns list of correctly named authors
    def test_api_returns_all_authors(self):
        url = reverse("work-detail", args=[self.work.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        names = {a["name"] for a in resp.data["authors"]}
        self.assertSetEqual(names, {"Author One", "Author Two"})

    #test the POST to create a new work-author tuple
    def test_create_work_author_link(self):
        response = self.client.post(
            reverse("workauthor-list"),
            data={"work": self.work.id, "author": self.author3.id},
            format="json"
        )
        #first insert should produce a 201
        self.assertEqual(response.status_code, 201)
        self.assertTrue(WorkAuthor.objects.filter(work=self.work, author=self.author3).exists())
        
    #test the POST cannot create a duplicate work-author tuple
    def test_cannot_duplicate_work_author_link(self):
        response = self.client.post(
            reverse("workauthor-list"),
            data={"work": self.work.id, "author": self.author1.id},
            format="json"
        )
        #Duplicate should produce a 400
        self.assertEqual(response.status_code, 400)
    
    #test the GET that lists all the work-author tuples
    def test_list_work_author_links(self):
        WorkAuthor.objects.create(work=self.work, author=self.author1)
        response = self.client.get(reverse("workauthor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    #test the DELETE of a work-author tuple
    def test_delete_work_author_link(self):
        link = WorkAuthor.objects.create(work=self.work, author=self.author1)
        url = reverse("workauthor-detail", args=[link.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WorkAuthor.objects.filter(id=link.id).exists())




