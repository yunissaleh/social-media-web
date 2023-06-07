from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Follows, Like
from django.http import JsonResponse
import json

def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(posts, 10)
    pg_num = request.GET.get('page')
    pg_posts = paginator.get_page(pg_num)

    likes = Like.objects.all()
    myLikes = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                myLikes.append(like.post.id)
    except:
      myLikes = []

    return render(request, "network/index.html", {
        "posts": pg_posts,
        "myLikes": myLikes
    })


def post(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        content = request.POST['content']
        post = Post(author=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))


def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    following = Follows.objects.filter(user=currentUser)
    followed_posts = []
    for follow in following:
        followed_posts += Post.objects.filter(author=follow.followed).order_by("id").reverse()

    likes = Like.objects.all()
    myLikes = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                myLikes.append(like.post.id)
    except:
        myLikes = []
    paginator = Paginator(followed_posts, 10)
    pg_num = request.GET.get('page')
    pg_posts = paginator.get_page(pg_num)
    return render(request, "network/following.html", {
        "posts": pg_posts,
        "myLikes": myLikes
    })


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user_posts = Post.objects.filter(author=user).order_by("id").reverse()
    paginator = Paginator(user_posts, 10)
    pg_num = request.GET.get('page')
    pg_posts = paginator.get_page(pg_num)

    following = Follows.objects.filter(user=user)
    follower = Follows.objects.filter(followed=user)

    checkFollow = follower.filter(user=User.objects.get(pk=request.user.id))
    if len(checkFollow) != 0:
        isFollowing = True
    else:
        isFollowing = False

    likes = Like.objects.all()
    myLikes = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                myLikes.append(like.post.id)
    except:
        myLikes = []

    return render(request, "network/profile.html", {
        "posts": pg_posts,
        "usern": user.username,
        "following": following,
        "follower": follower,
        "isFollowing": isFollowing,
        "profile_user": user,
        "myLikes": myLikes
    })


def unfollow(request):
    currentUser = User.objects.get(pk=request.user.id)
    profile_user = User.objects.get(username=request.POST['userfollow'])
    f = Follows.objects.get(user=currentUser, followed=profile_user)
    f.delete()
    profile_id = profile_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': profile_id}))


def follow(request):
    currentUser = User.objects.get(pk=request.user.id)
    profile_user = User.objects.get(username=request.POST['userfollow'])
    f = Follows(user=currentUser, followed=profile_user)
    f.save()
    profile_id = profile_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': profile_id}))

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.content = data["content"]
        post.save()
        return JsonResponse({"message":"Successful edit", "data":data["content"]})

def like(request, post_id, bool):
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=request.user.id)
        message = ""
        if bool:
            like = Like(user=user,post=post)
            like.save()
            message = "like added"
        else:
            like = Like.objects.filter(user=user,post=post)
            like.delete()
            message = "like removed"

        return JsonResponse({"message":message})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
