from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        testuser = User.objects.create_user(
            username="deepak", password="12345"
        )
        Post.objects.create(
            title="Sample Test",
            body="I am Testing",
            author=testuser,
            status="draft",
        )
        Post.objects.create(
            title="Sample Test 2",
            body="I am Testing 2",
            author=testuser,
            status="published",
        )


    def test_published_manager(self):
        published_queryset = Post.published.get_queryset()
        objects_queryset_with_status_published = Post.objects.filter(
            status="published"
        )
        self.assertQuerysetEqual(
            published_queryset, objects_queryset_with_status_published
        )
