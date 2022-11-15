from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User
from django.urls import reverse


class TestPostView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="deepak", password="root"
        )
        self.unpublished_post = Post.objects.create(
            title="Test post that's status=draft by default",
            author=self.user,
            body="This post is created by testuser author",
        )
        self.published_post = Post.objects.create(
            title="Test post that's status=published",
            author=self.user,
            body="This post is created by testuser author",
            slug="post-created-testuser-author",
            status="published",
        )

    def test_post_list_template_used(self):
        post_list_url = reverse("blog:post_list")
        response = self.client.get(post_list_url)

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
