from django.test import TestCase
from blog.models import Post
from django.urls import reverse
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class PostViewsTest(ModelMixinTestCase, TestCase):
    def test_post_list_template_used(self):
        self.post_list_url = reverse("blog:post_list")
        response = self.client.get(self.post_list_url)

        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_post_list_should_return_status_200_GET(self):
        self.post_list_url = reverse("blog:post_list")
        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_used(self):
        response = self.client.get(self.post_detail_url)

        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_post_detail_should_return_200_for_valid_post(self):
        response = self.client.get(self.post_detail_url)

        self.assertEqual(200, response.status_code)

    def test_post_detail_should_return_404_for_invalid_post(self):

        incorrect_year = "2093"
        incorrect_month = "12"
        incorrect_day = "7"
        incorrect_slug = "incorrect_slug"

        incorrect_post_detail_url = (
            "http://127.0.0.1:8000/blog/{year}/{month}/{day}/{slug}/".format(
                year=incorrect_year,
                month=incorrect_month,
                day=incorrect_day,
                slug=incorrect_slug,
            )
        )
        unsuccessful_response = self.client.get(incorrect_post_detail_url)

        self.assertEqual(404, unsuccessful_response.status_code)

    def test_post_share_template_used(self):
        response = self.client.get(self.post_share_url)

        self.assertTemplateUsed(response, "blog/post/share.html")
