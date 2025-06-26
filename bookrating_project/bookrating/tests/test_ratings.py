from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from bookrating.factories import BookEditionFactory
from bookrating.models import Rating


class RatingAPITest(APITestCase):
    def setUp(self):
        self.user_id = 42
        self.edition = BookEditionFactory()
        # self.rating = Rating.objects.create(
        #    user_id=self.user_id, edition=self.edition, rating=3
        # )
        self.rating_url = reverse("rating-list")

        # self.rating_url_detail = reverse(
        #    "rating-detail", args=[self.rating.id])

    def test_create_valid_rating(self):
        url = reverse("rating-list")
        data = {"user_id": self.user_id,
                "edition": self.edition.id, "rating": 4}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rating_below_range(self):
        url = reverse("rating-list")
        data = {"edition": self.edition.id, "rating": -1}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rating", response.data)

    # def test_rating_above_range(self):
    #     url = reverse("rating-list")
    #     data = {"edition": self.edition.id, "rating": 6}
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("rating", response.data)

    # def test_rating_non_integer(self):
    #     url = reverse("rating-list")
    #     data = {"edition": self.edition.id, "rating": "not-a-number"}
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("rating", response.data)

    # def test_put_valid_rating(self):
    #     url = reverse("rating-detail", args=[self.rating.id])
    #     data = {"edition": self.edition.id, "rating": 5}
    #     response = self.client.put(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.rating.refresh_from_db()
    #     self.assertEqual(self.rating.rating, 5)

    # def test_patch_valid_rating(self):
    #     url = reverse("rating-detail", args=[self.rating.id])
    #     data = {"rating": 2}
    #     response = self.client.patch(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.rating.refresh_from_db()
    #     self.assertEqual(self.rating.rating, 2)

    # def test_put_invalid_rating(self):
    #     url = reverse("rating-detail", args=[self.rating.id])
    #     data = {"edition": self.edition.id, "rating": 99}  # invalid
    #     response = self.client.put(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("rating", response.data)

    # def test_patch_invalid_rating(self):
    #     url = reverse("rating-detail", args=[self.rating.id])
    #     data = {"rating": -3}
    #     response = self.client.patch(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("rating", response.data)

    # def test_create_duplicate_rating_fails(self):
    #     data = {"edition": self.edition.id, "rating": 5}
    #     response = self.client.post(self.rating_url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("non_field_errors", response.data)

    # def test_delete_rating(self):
    #     url = reverse("rating-detail", args=[self.rating.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Rating.objects.filter(id=self.rating.id).exists())
