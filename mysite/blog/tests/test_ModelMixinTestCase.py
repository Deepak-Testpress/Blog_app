from django.test import TestCase, Client
from blog.models import Post
from django.urls import reverse
from django.contrib.auth.models import User


class ModelMixinTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.published_queryset = Post.published.get_queryset()
        self.post_objects_with_status_published_queryset = Post.objects.filter(
            status="published"
        )

        self.test_user = User.objects.create_user(
            username="deepak",
            password="root",
        )

        self.test_draft_post = Post.objects.create(
            title="Test post thats status=draft by default",
            author=self.test_user,
            body="This post is created by testuser author",
        )
        self.test_published_post = Post.objects.create(
            title="Test post thats status=published",
            author=self.test_user,
            body="This post is created by testuser author",
            slug="post-created-testuser-author",
            status="published",
        )

        self.post_list_url = reverse("blog:post_list")
        self.post_detail_url = reverse(
            "blog:post_detail",
            args=[
                self.test_published_post.publish.year,
                self.test_published_post.publish.month,
                self.test_published_post.publish.day,
                self.test_published_post.slug,
            ],
        )
        self.post_share_url = reverse("blog:post_share", args=[2])
