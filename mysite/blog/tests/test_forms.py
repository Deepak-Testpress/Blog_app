from django.test import TestCase
from blog.forms import CommentForm, EmailPostForm
from blog.views import post_share, post_detail
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.http import HttpRequest
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class TestForms(ModelMixinTestCase, TestCase):
    # @classmethod
    # def setUpTestData(cls):

    #     testuser = User.objects.create_user(username="deepak", password="root")
    #     Post.objects.create(
    #         title="Sample Test",
    #         body="I am Testing",
    #         author=testuser,
    #         status="published",
    #         slug="slug",
    #     )

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

    def test_comment_form_valid_data(self):
        form = CommentForm(
            data={
                "post": self.test_published_post,
                "name": "First comment",
                "email": "deeepak@testpress.in",
                "body": "this is comment body",
            }
        )
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid_data(self):
        form = CommentForm(
            data={
                "post": self.test_published_post,
                "name": "First comment",
                "email": "invalid-email",
                "body": "this is comment body",
            }
        )
        self.assertFalse(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())

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
        post_id = self.test_published_post.id
        response = post_share(request=request, post_id=post_id)
        self.assertEqual(200, response.status_code)

    def test_post_detail_should_return_200_with_valid_post_obj(self):

        request = HttpRequest()
        request.method = "POST"
        request.META = {
            "SERVER_NAME": "testserver",
            "SERVER_PORT": "8000",
        }
        request.POST = {
            "post": self.test_published_post,
            "name": "Test comment",
            "email": "deepak@testpress.in",
            "body": "this is comment body",
        }

        response = post_detail(
            request=request,
            year=self.test_published_post.publish.year,
            month=self.test_published_post.publish.month,
            day=self.test_published_post.publish.day,
            post=self.test_published_post.slug,
        )
        comment = self.test_post_comment
        post = self.test_published_post

        self.assertEqual(post, comment.post)
        self.assertEqual(200, response.status_code)
