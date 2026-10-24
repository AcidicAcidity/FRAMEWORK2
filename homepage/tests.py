from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from homepage import views


class HomepageTests(TestCase):
    def test_index_uses_templates(self):
        response = self.client.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")
        self.assertContains(response, "<title>")
        self.assertContains(response, "Главная – Каршеринг")

    def test_base_links_static_files(self):
        response = self.client.get("/")
        self.assertContains(response, "/static/homepage/css/style.css")
        self.assertContains(response, "/static/homepage/img/logo.png")
        self.assertContains(response, "/static/homepage/js/main.js")

    def test_static_files_exist(self):
        for name in ("css/style.css", "js/main.js", "img/logo.png"):
            self.assertIsNotNone(finders.find(f"homepage/{name}"), name)

    def test_navigation_links_built_by_url_tag(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="/cars/"')
        self.assertContains(response, 'href="/trips/"')

    def test_unknown_url_uses_custom_404_template(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(
            response, "404 – страница не найдена", status_code=404
        )

    def test_page_function_removed(self):
        self.assertFalse(hasattr(views, "page"))
