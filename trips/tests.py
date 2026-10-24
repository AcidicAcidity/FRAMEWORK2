from django.test import TestCase


class TripsViewsTests(TestCase):
    def test_list(self):
        response = self.client.get("/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10.10.2026")

    def test_detail_active(self):
        response = self.client.get("/trips/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мария Кузнецова")
        self.assertContains(response, "3800 руб.")

    def test_detail_cancelled(self):
        response = self.client.get("/trips/3/")
        self.assertContains(response, "отменена")

    def test_missing_trip_404(self):
        response = self.client.get("/trips/999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Поездка не найдена", status_code=404)
