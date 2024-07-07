from django.test import TestCase
from django.urls import reverse

from mysite.models import Comment, Like, Post, User


class PostModelTests(TestCase):

    def test_post_creation(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Test Content")
        self.assertEqual(post.comment_count, 0)
        self.assertEqual(post.like_count, 0)


class CommentModelTests(TestCase):

    def test_comment_creation(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        comment = Comment.objects.create(post=post, text="Test Comment")
        self.assertEqual(comment.text, "Test Comment")
        self.assertEqual(comment.post, post)


class LikeModelTests(TestCase):

    def test_like_creation(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        like = Like.objects.create(post=post, user=user)
        self.assertEqual(like.post, post)
        self.assertEqual(like.user, user)


class PostListViewTests(TestCase):

    def test_no_posts(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_post_list(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["title"], post.title)


class PostDetailViewTests(TestCase):

    def test_post_detail(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        response = self.client.get(reverse("post_detail", args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], post.title)
        self.assertEqual(response.json()["content"], post.content)
        self.assertEqual(response.json()["comment_count"], 0)
        self.assertEqual(response.json()["like_count"], 0)
        self.assertEqual(response.json()["comments"], [])


class AddCommentViewTests(TestCase):

    def test_add_comment(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        response = self.client.post(
            reverse("add_comment", args=[post.pk]),
            {"text": "Test Comment"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "Test Comment")
        post.refresh_from_db()
        self.assertEqual(post.comments.count(), 1)
        self.assertEqual(post.comment_count, 1)


class AddLikeViewTests(TestCase):

    def test_add_like(self):
        user = User.objects.create(username="testuser")
        post = Post.objects.create(user=user, title="Test Post", content="Test Content")
        response = self.client.post(
            reverse("add_like", args=[post.pk]),
            {"user_id": user.id},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(post.like_count, 1)
