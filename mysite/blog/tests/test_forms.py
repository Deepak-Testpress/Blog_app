from django.test import TestCase
from blog.forms import EmailPostForm
from blog.views import post_share
from blog.models import Post
from django.contrib.auth.models import User
from django.http import HttpRequest
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase
from django.contrib import messages


class TestEmailPostForm(ModelMixinTestCase, TestCase):
    def test_email_form_validation_returns_true_with_valid_form_data(self):
        form = EmailPostForm(
            data={
                "from_name": "Deepak",
                "from_email": "deepak@testpress.in",
                "to_email": "deepakadishankar@gmail.com",
                "share_message": "The post was awesome",
            }
        )

        self.assertTrue(form.is_valid())

    def test_email_form_validation_returns_false_with_invalid_form_data(self):
        form = EmailPostForm(
            data={
                "from_name": "Deepak",
                "from_email": "invalid_email",
                "to_email": "invalid_email",
                "share_message": "the share message can be anything in ",
            }
        )

        self.assertFalse(form.is_valid())

    def test_email_form_validation_returns_false_and_throws_errors_with_no_data(
        self,
    ):
        form = EmailPostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_post_share_should_return_200_with_valid_post_obj(self):

        request = HttpRequest()
        request.method = "POST"
        request.META = {
            "SERVER_NAME": "testserver",
            "SERVER_PORT": "8000",
        }
        request.POST = {
            "from_name": "Deepak",
            "from_email": "deepak@testpress.in",
            "to_email": "deepakadishankar@gmail.com",
            "share_message": "The post was awesome",
        }
        request._messages = messages.storage.default_storage(request)
        response = post_share(request=request, post_id=self.published_post.id)
        self.assertEqual(200, response.status_code)
