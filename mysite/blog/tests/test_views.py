from django.test import TestCase, Client
from blog.models import Post, User
from django.urls import reverse
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class TestPostView(ModelMixinTestCase, TestCase):
    def test_post_list_template_used(self):
        self.post_list_url = reverse("blog:post_list")
        response = self.client.get(self.post_list_url)

        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_post_detail_template_used(self):
        post_detail_url = reverse(
            "blog:post_detail",
            args=[
                self.published_post.publish.year,
                self.published_post.publish.month,
                self.published_post.publish.day,
                self.published_post.slug,
            ],
        )
        response = self.client.get(post_detail_url)

        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_post_detail_should_return_404_for_invalid_post_args(self):

        post_detail_url = reverse(
            "blog:post_detail",
            args=[
                "2093",
                "12",
                "12",
                "slug-that-does-not-exist",
            ],
        )
        response = self.client.get(post_detail_url)

        self.assertEqual(404, response.status_code)

    def test_post_share_template_used(self):
        response = self.client.get(self.post_share_url)

        self.assertTemplateUsed(response, "blog/post/share.html")
