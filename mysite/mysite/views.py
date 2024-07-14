import re

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import (
    Comment,
    Like,
    Post,
    TrendingTopic,
    get_trending_topics,
    update_trending_topics,
)

User = get_user_model()


def extract_tags(text: str) -> list[str]:
    """Extracts topics from a text

    Parameters
    ----------
    text : str
        This is the text to look for topics

    Returns
    -------
    list[str]
        Topics
    """
    # Regex pattern to find hashtags in the text
    return re.findall(r"#\w+", text)


def update_trending_topics_from_text(text: str) -> None:
    hashtags = extract_tags(text)
    for hashtag in hashtags:
        trending_topic, created = TrendingTopic.objects.get_or_create(topic=hashtag)
        if not created:
            trending_topic.count += 1
        trending_topic.save()


@login_required
def post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            update_trending_topics_from_text(post.content)
            return redirect("post_list")
    else:
        form = PostForm()
    posts = Post.objects.all()
    trending_topics = TrendingTopic.objects.all().order_by("-count")[:10]
    return render(
        request,
        "mysite/post_list.html",
        {
            "posts": posts,
            "form": form,
            "trending_topics": trending_topics,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    trending_topics = TrendingTopic.objects.all().order_by("-count")[:10]
    return render(
        request,
        "mysite/post_detail.html",
        {"post": post, "comments": comments, "trending_topics": trending_topics},
    )


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the user directly
            post.save()
            update_trending_topics_from_text(post.content)
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "mysite/add_post.html", {"form": form})


@csrf_exempt
def add_comment(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get("text")
        if text:
            comment = Comment.objects.create(post=post, text=text)
            update_trending_topics_from_text(text)
            post.comment_count = post.comments.count()
            post.save()
        return redirect("post_detail", pk=post.pk)
    return HttpResponse(status=405)


@csrf_exempt
def add_like(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        user = request.user  # Assign the user directly
        if not Like.objects.filter(post=post, user=user).exists():
            Like.objects.create(post=post, user=user)
            post.like_count = post.likes.count()
            post.save()
        return redirect("post_detail", pk=post.pk)
    return HttpResponse(status=405)
