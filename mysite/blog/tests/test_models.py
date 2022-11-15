from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(self):

        testuser = User.objects.create_user(username="deepak", password="root")

        self.draft_post = Post.objects.create(
            title="Test that's status=draft by default",
            body="its a draft post with id=1",
            author=testuser,
        )
        self.published_post = Post.objects.create(
            title="Sample Test 2",
            body="its a published post with id=2",
            author=testuser,
            status="published",
        )

    def test_post_str_method_returns_post_title(self):

        self.assertEqual(str(self.draft_post), self.draft_post.title)

    def test_published_manager_returns_all_published_posts(self):
        published_manager_result = Post.published.all()
        posts_with_status_published = Post.objects.filter(status="published")
        self.assertQuerysetEqual(
            published_manager_result, posts_with_status_published
        )
