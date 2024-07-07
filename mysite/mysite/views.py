from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import Comment, Like, Post, User

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, "mysite/post_list.html", {"posts": posts})


@login_required
def post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user.id = request.user.id
            post.save()
            return redirect("post_list")
    else:
        form = PostForm()
    posts = Post.objects.all()
    return render(request, "mysite/post_list.html", {"posts": posts, "form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(
        request, "mysite/post_detail.html", {"post": post, "comments": comments}
    )


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user.id = (
                request.user.id
                if request.user.id.is_authenticated
                else get_object_or_404(User, username="defaultuser")
            )
            post.save()
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
            post.comment_count = post.comments.count()
            post.save()
        return redirect("post_detail", pk=post.pk)
    return HttpResponse(status=405)


@csrf_exempt
def add_like(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        user = (
            request.user.id
            if request.user.is_authenticated
            else get_object_or_404(User, username="defaultuser")
        )
        Like.objects.create(post=post, user=request.user)
        post.like_count = post.likes.count()
        post.save()
        return redirect("post_detail", pk=post.pk)
    return HttpResponse(status=405)
