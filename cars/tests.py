from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from models import Car, User


class CarsViewsTests(TestCase):
    def test_list(self):
        response = self.client.get(reverse("cars:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cars/car_list.html")
        self.assertTemplateUsed(response, "cars/includes/car_card.html")
        self.assertContains(response, "Toyota Camry")
        self.assertContains(response, "Всего автомобилей: 4")
        self.assertEqual(len(response.context["cars"]), 4)

    def test_list_empty(self):
        with patch("cars.views.load_cars", return_value=[]):
            response = self.client.get(reverse("cars:list"))
        self.assertContains(response, "Автомобили не найдены.")

    def test_detail(self):
        response = self.client.get(reverse("cars:detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cars/car_detail.html")
        self.assertContains(response, "Иван Петров")
        self.assertContains(response, "скидка 5%")
        self.assertContains(response, "скидка 15%")

    def test_unavailable_car(self):
        response = self.client.get(reverse("cars:detail", args=[4]))
        self.assertContains(response, "недоступен для аренды")

    def test_missing_car_404(self):
        response = self.client.get(reverse("cars:detail", args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response, "Автомобиль не найден", status_code=404
        )

    def test_non_int_id_not_routed(self):
        self.assertEqual(self.client.get("/cars/abc/").status_code, 404)

    def test_html_is_escaped(self):
        owner = User(1, "Иван", "i@example.com")
        car = Car(1, "<b>Evil</b>", "X", "A1", owner, 100)
        with patch("cars.views.load_cars", return_value=[car]):
            response = self.client.get(reverse("cars:list"))
        self.assertNotContains(response, "<b>Evil</b>")
        self.assertContains(response, "&lt;b&gt;Evil&lt;/b&gt;")
