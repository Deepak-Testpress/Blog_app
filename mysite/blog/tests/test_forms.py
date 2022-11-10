from django.test import TestCase
from blog.forms import EmailPostForm
from blog.views import post_share
from blog.models import Post
from django.contrib.auth.models import User
from django.http import HttpRequest


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):

        testuser = User.objects.create_user(username="deepak", password="root")
        Post.objects.create(
            title="Sample Test",
            body="I am Testing",
            author=testuser,
            status="published",
            slug="slug",
        )

    def test_email_form_valid_data(self):
        form = EmailPostForm(
            data={
                "name": "Deepak",
                "email": "deepak@testpress.in",
                "to": "deepakadishankar@gmail.com",
                "comments": "The post was awesome",
            }
        )

        self.assertTrue(form.is_valid())

    def test_email_form_invalid_data(self):
        form = EmailPostForm(
            data={
                "name": "Deepak",
                "email": "invalid-email",
                "to": "deepakadishankar@gmail.com",
                "comments": "The post was awesome",
            }
        )

        self.assertFalse(form.is_valid())

    def test_Email_form_no_data(self):
        form = EmailPostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertRaises(TypeError)
        self.assertRaises(ValueError)
        self.assertRaises(KeyError)

    def test_post_share_should_return_200_with_valid_post_obj(self):

        request = HttpRequest()
        request.method = "POST"
        request.META = {
            "SERVER_NAME": "testserver",
            "SERVER_PORT": "8000",
        }
        request.POST = {
            "name": "Deepak",
            "email": "deepak@testpress.in",
            "to": "deepakadishankar@gmail.com",
            "comments": "The post was awesome",
        }
        post_id = 1
        res = post_share(request=request, post_id=post_id)
        self.assertEqual(200, res.status_code)
