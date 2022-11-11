from django.test import TestCase
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase


class PostModelTest(ModelMixinTestCase, TestCase):
    def test_post_object_name_is_title(self):
        self.assertEqual(
            str(self.test_draft_post),
            "Test post thats status=draft by default",
        )

    def test_published_manager(self):
        self.assertQuerysetEqual(
            self.published_queryset,
            self.post_objects_with_status_published_queryset,
        )


class CommentModelTest(ModelMixinTestCase, TestCase):
    def test_comment_object_name_is_title(self):
        self.assertEqual(
            str(self.test_post_comment),
            f"Comment by {self.test_post_comment.name} on {self.test_post_comment.post}",
        )
