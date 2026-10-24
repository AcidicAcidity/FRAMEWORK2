from django.test import TestCase


class CarsViewsTests(TestCase):
    def test_list(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota Camry")

    def test_detail(self):
        response = self.client.get("/cars/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иван Петров")

    def test_unavailable_car_is_busy(self):
        response = self.client.get("/cars/4/")
        self.assertContains(response, "занят")

    def test_missing_car_404(self):
        response = self.client.get("/cars/999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response, "Автомобиль не найден", status_code=404
        )

    def test_non_int_id_not_routed(self):
        self.assertEqual(self.client.get("/cars/abc/").status_code, 404)
