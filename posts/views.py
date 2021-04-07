from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .apps import PostsConfig
from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def index(request):
    post_list = Post.objects.select_related("group")
    paginator = Paginator(post_list, PostsConfig.pages_on_list)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {
        "page": page,
        "paginator": paginator
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, PostsConfig.pages_on_list)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {
        "group": group,
        "page": page,
        "paginator": paginator
    })


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    title_0 = "Новый пост"
    title_1 = "Новая запись"
    title_2 = "Добавить"
    return render(request, "new.html", {
        "form": form,
        "title_0": title_0,
        "title_1": title_1,
        "title_2": title_2
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, PostsConfig.pages_on_list)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        follower_list = request.user.follower.values_list("author_id",
                                                          flat=True)
        if author.id in follower_list:
            following = True
    return render(
        request,
        "profile.html",
        {
            "page": page,
            "paginator": paginator,
            "author": author,
            "following": following,
        }
    )


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    comment_list = post.comments.all()
    form = CommentForm(request.POST or None)
    following = False
    if request.user.is_authenticated:
        follower_list = request.user.follower.values_list("author_id",
                                                          flat=True)
        if author.id in follower_list:
            following = True
    return render(
        request,
        "post.html",
        {
            "post": post,
            "author": post.author,
            "comments": comment_list,
            "form": form,
            "following": following,
        }
    )


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if post.author != request.user:
        return redirect("post", username=username, post_id=post_id)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post", username=username, post_id=post_id)
    title_0 = "Редактирование поста"
    title_1 = "Редактировать запись"
    title_2 = "Сохранить"
    return render(request, "new.html", {
        "form": form,
        "post": post,
        "title_0": title_0,
        "title_1": title_1,
        "title_2": title_2
    })


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    comment_list = post.comments.all()
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post_id = post_id
        comment.save()
        return redirect("post", username=username, post_id=post_id)
    return render(request, "comments.html", {
        "form": form,
        "comments": comment_list
    })


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, PostsConfig.pages_on_list)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {
        "page": page,
        "paginator": paginator,
    })


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("profile", username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username)
