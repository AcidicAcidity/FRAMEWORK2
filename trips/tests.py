from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TripsViewsTests(TestCase):
    def test_list(self):
        response = self.client.get(reverse("trips:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/trip_list.html")
        self.assertTemplateUsed(response, "trips/includes/trip_status.html")
        self.assertContains(response, "Всего поездок: 3")
        self.assertContains(response, "10.10.2026")

    def test_list_empty(self):
        with patch("trips.views.load_trips", return_value=[]):
            response = self.client.get(reverse("trips:list"))
        self.assertContains(response, "Поездки не найдены.")

    def test_detail_active(self):
        response = self.client.get(reverse("trips:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мария Кузнецова")
        self.assertContains(response, "3800 руб.")
        self.assertContains(response, "Активна")

    def test_detail_cancelled(self):
        response = self.client.get(reverse("trips:detail", args=[3]))
        self.assertContains(response, "Отменена")

    def test_missing_trip_404(self):
        response = self.client.get(reverse("trips:detail", args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Поездка не найдена", status_code=404)
