from rest_framework.test import APITestCase
from django.urls import reverse

from bookrating.models import Work
from bookrating.factories import WorkFactory

class WorkAPITest(APITestCase):
    def setUp(self):
        self.work = WorkFactory()

    def test_get_work(self):
        url = reverse("work-detail", args=[self.work.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.work.title)

    def test_update_work(self):
        url = reverse("work-detail", args=[self.work.pk])
        new_data = {
            "id": self.work.id,
            "title": "Updated Title",
            "original_year": 1999,
            "avg_rating": "4.5",
            "ratings_count": 1234,
        }
        response = self.client.put(url, new_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.work.refresh_from_db()
        self.assertEqual(self.work.title, "Updated Title")

    def test_delete_work(self):
        url = reverse("work-detail", args=[self.work.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Work.objects.filter(pk=self.work.pk).exists())

    def test_create_work(self):
        url = reverse("work-list")
        data = {
            "id": 9999,
            "title": "New Work",
            "original_year": 2023,
            "avg_rating": "4.0",
            "ratings_count": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Work.objects.filter(title="New Work").exists())
