from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class PostModelTest(ModelMixinTestCase, TestCase):
    def test_post_str_method_returns_post_title(self):

        self.assertEqual(str(self.draft_post), self.draft_post.title)

    def test_published_manager_returns_all_published_posts(self):
        published_manager_result = Post.published.all()
        posts_with_status_published = Post.objects.filter(status="published")
        self.assertQuerysetEqual(
            published_manager_result, posts_with_status_published
        )
