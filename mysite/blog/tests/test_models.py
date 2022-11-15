from django.test import TestCase
from blog.tests.test_ModelMixinTestCase import ModelMixinTestCase
from django.db.models.query import EmptyQuerySet
from django.db.models import Model
from blog.models import Post


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

    def test_get_top_four_similar_posts_returns_empty_queryset_with_only_one_tagged_post(
        self,
    ):

        similar_posts = (
            self.test_first_published_post_with_tag.get_top_four_similar_posts()
        )
        self.assertFalse(similar_posts.exists())

    def test_get_top_four_similar_posts_returns_posts_queryset_with_posts_with_same_tag_excluding_self_post(
        self,
    ):
        self.test_second_published_post_with_tag.tags.add("test")
        similar_posts = (
            self.test_first_published_post_with_tag.get_top_four_similar_posts()
        )
        self.assertEqual(
            self.test_second_published_post_with_tag, similar_posts.first()
        )


class CommentModelTest(ModelMixinTestCase, TestCase):
    def test_comment_object_name_is_title(self):
        self.assertEqual(
            str(self.test_post_comment),
            f"Comment by {self.test_post_comment.name} on {self.test_post_comment.post}",
        )
