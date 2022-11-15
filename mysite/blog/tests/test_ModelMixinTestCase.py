from django.test import TestCase, Client
from blog.models import Post, Comment
from django.urls import reverse
from taggit.managers import TaggableManager
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
        self.test_first_published_post_with_tag = Post.objects.create(
            title="First post that will have tag",
            author=self.test_user,
            body="This post is created by testuser author",
            slug="second-post-with-tag",
            status="published",
        )
        self.test_first_published_post_with_tag.tags.add("test")

        self.test_second_published_post_with_tag = Post.objects.create(
            title="Second Test post that will have tag",
            author=self.test_user,
            body="This post is created by testuser author",
            slug="second-post-with-tag",
            status="published",
        )

        # self.test_second_published_post_with_tag.tags.add("poda")

        # self.published_post3_with_tag = Post.objects.create(
        #     title="Third Test post thats tag=eco",
        #     author=self.test_user,
        #     body="This post is created by testuser author",
        #     slug="third-post-with-tag",
        #     status="published",
        # )
        # self.published_post3_with_tag.tags.add("echo")

        # self.published_post4_with_tag = Post.objects.create(
        #     title="Fourth Test post thats tag=eco",
        #     author=self.test_user,
        #     body="This post is created by testuser author",
        #     slug="fourth-post-with-tag",
        #     status="published",
        # )
        # self.published_post4_with_tag.tags.add("echo","echo2")

        # self.published_post5_with_tag = Post.objects.create(
        #     title="Fifth Test post thats tag=eco",
        #     author=self.test_user,
        #     body="This post is created by testuser author",
        #     slug="fifth-post-with-tag",
        #     status="published",
        # )
        # self.published_post5_with_tag.tags.add("echo")

        # self.published_post6_with_tag = Post.objects.create(
        #     title="Sixth Test post thats tag=eco",
        #     author=self.test_user,
        #     body="This post is created by testuser author",
        #     slug="sixth-post-with-tag",
        #     status="published",
        # )
        # self.published_post6_with_tag.tags.add("echo")

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

        self.test_post_comment = Comment.objects.create(
            post=self.test_published_post,
            name="First comment",
            email="deeepak@testpress.in",
            body="this is comment body",
        )
