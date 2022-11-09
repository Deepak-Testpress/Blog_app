from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User
from django.urls import reverse


class PostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.objects.create_user(
            username="deepak", password="root"
        )
        self.test_post = Post.objects.create(
            title="Test post thats status=draft by default",
            author=self.test_user,
            body="This post is created by testuser author",
        )
        self.published_post = Post.objects.create(
            title="Test post thats status=published",
            author=self.test_user,
            body="This post is created by testuser author",
            slug="post-created-testuser-author",
            status="published",
        )

    def test_post_list_template_used(self):
        post_list_url = reverse("blog:post_list")
        response = self.client.get(post_list_url)

        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_post_list_should_return_status_200(self):
        post_list_url = reverse("blog:post_list")
        response = self.client.get(post_list_url)

        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_used(self):
        published_post = Post.objects.get(id=2)

        year = published_post.publish.year
        month = published_post.publish.month
        day = published_post.publish.day
        slug = published_post.slug

        post_detail_url = (
            "http://127.0.0.1:8000/blog/{year}/{month}/{day}/{slug}/".format(
                year=year, month=month, day=day, slug=slug
            )
        )

        response = self.client.get(post_detail_url)

        self.assertTemplateUsed(response, "blog/post/detail.html")

    def test_post_detail_should_return_200_for_valid_post(self):

        published_post = Post.objects.get(id=2)

        year = published_post.publish.year
        month = published_post.publish.month
        day = published_post.publish.day
        slug = published_post.slug

        post_detail_url = (
            "http://127.0.0.1:8000/blog/{year}/{month}/{day}/{slug}/".format(
                year=year, month=month, day=day, slug=slug
            )
        )

        successful_response = self.client.get(post_detail_url)

        self.assertEqual(200, successful_response.status_code)
        self.assertEqual(
            Post.objects.first().title, "Test post thats status=published"
        )

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
