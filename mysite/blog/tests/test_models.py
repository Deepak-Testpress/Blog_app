from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        testuser = User.objects.create_user(username="deepak", password="root")
        Post.objects.create(
            title="Sample Test",
            body="I am Testing",
            author=testuser,
            status=Post.STATUS_CHOICES[0][0],
        )
        Post.objects.create(
            title="Sample Test 2",
            body="I am Testing 2",
            author=testuser,
            status=Post.STATUS_CHOICES[1][0],
        )

    def test_post_getters(self):
        post = Post.objects.get(id=1)
        testuser = User.objects.get(id=1)
        self.assertEqual(str(post.title), "Sample Test")
        self.assertEqual(str(post.body), "I am Testing")
        self.assertEqual(str(post.status), "draft")
        self.assertEqual(post.author, testuser)

    def test_post_field_structure(self):
        post = Post.objects.get(id=1)
        title_max_length = post._meta.get_field("title").max_length
        self.assertEqual(title_max_length, 250)
        slug_max_length = post._meta.get_field("slug").max_length
        self.assertEqual(slug_max_length, 250)
        status_max_length = post._meta.get_field("status").max_length
        self.assertEqual(status_max_length, 10)

    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), "Sample Test")

    def test_published_manager(self):
        published_queryset = Post.published.get_queryset()
        objects_queryset_with_status_published = Post.objects.filter(
            status="published"
        )
        self.assertQuerysetEqual(
            published_queryset, objects_queryset_with_status_published
        )
