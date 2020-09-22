from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import User, Post, Like, Follow


def index(request):
    try:
        current_user = User.objects.get(pk=request.user.id)
        posts = Post.objects.all().order_by("-post_timestamp")
        for post in posts:
            post.serialize()
            if post.post_user.id == request.user.id:
                post.editable = True
            else:
                post.editable = False
            try:
                if_liked = Like.objects.get(like_post=post.id, like_by=current_user)
                post.liked_by_user = True
            except:
                post.liked_by_user = False
        paginator_posts = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        try:
            posts = paginator_posts.page(page)
        except EmptyPage:
            posts = paginator_posts.page(paginator_posts.num_pages)
        except PageNotAnInteger:
            posts = paginator_posts.page(1)
        return render(request, "network/index.html", {
            "posts": posts
        })
    except:
        posts = Post.objects.all().order_by("-post_timestamp")
        for post in posts:
            post.serialize()
        paginator_posts = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        try:
            posts = paginator_posts.page(page)
        except EmptyPage:
            posts = paginator_posts.page(paginator_posts.num_pages)
        except PageNotAnInteger:
            posts = paginator_posts.page(1)
        return render(request, "network/index.html", {
            "posts": posts
        })


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

@login_required(login_url='/login', redirect_field_name=None)
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        if not request.body:
            return HttpResponse()
        else: 
            data = json.loads(request.body)
            user = User.objects.get(pk=request.user.id)
            post = Post(post_user=user, post_content=data['post_content'])
            post.save()
            return JsonResponse({
                "message": "Posted successfully.",
                "post_content": post.post_content,
                "post_user": user.username,
                "post_timestamp": post.post_timestamp.strftime("%b %#d %Y, %#I:%M %p"),
                "post_id": post.id,
            }, status=200)

@login_required(login_url='/login', redirect_field_name=None)
def profile(request):
    user = User.objects.get(pk=request.user.id)
    posts = Post.objects.filter(post_user=user).order_by("-post_timestamp")
    current_user = User.objects.get(pk=request.user.id)
    # Check if post is liked by the current user
    for post in posts:
        try:
            if_liked = Like.objects.get(like_post=post.id, like_by=user)
            post.liked_by_user = True
        except:
            post.liked_by_user = False
    page = request.GET.get('page')
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    followers = Follow.objects.filter(follow_following=user).count() # People that follow the user
    following = Follow.objects.filter(follow_user=user).count() # People that the user follows
    return render(request, "network/user.html", {
        "profile": True,
        "posts": posts,
        "followers": followers,
        "following": following,
        "editable": True
    })

@login_required(login_url='/login', redirect_field_name=None)
def user(request, id):
    if id == request.user.id:
        return HttpResponseRedirect(reverse("profile"))
    else:
        user = User.objects.get(pk=id)
        posts = Post.objects.filter(post_user=user).order_by("-post_timestamp")
        followers = Follow.objects.filter(follow_following=user).count()
        following = Follow.objects.filter(follow_user=user).count()
        current_user = User.objects.get(pk=request.user.id)
        # Check if post is liked by the current user
        for post in posts:
            try:
                if_liked = Like.objects.get(like_post=post.id, like_by=current_user)
                post.liked_by_user = True
            except:
                post.liked_by_user = False

        # Check if the current user is already following
        try:
            current_following = Follow.objects.get(follow_user=current_user, follow_following=user)
            is_following = True
        except:
            is_following = False
        paginator_posts = Paginator(posts, 10)
        page = request.GET.get('page', 1)
        try:
            posts = paginator_posts.page(page)
        except EmptyPage:
            posts = paginator_posts.page(paginator_posts.num_pages)
        except PageNotAnInteger:
            posts = paginator_posts.page(1)
        
        return render(request, "network/user.html", {
            "profile": False,
            "is_following": is_following,
            "posts": posts,
            "followers": followers,
            "following": following,
            "editable": False,
            "user_visited": user,
        })

@login_required(login_url='/login', redirect_field_name=None)
@csrf_exempt
def follow(request, id):
    current_user = User.objects.get(pk=request.user.id)
    user_tofollow = User.objects.get(pk=id)
    try:
        is_following = Follow.objects.get(follow_user=current_user, follow_following=user_tofollow)
        is_following.delete()
        follow_counter = Follow.objects.filter(follow_following=user_tofollow).count()
        return JsonResponse({
            "message": "User unfollowed.",
            "followers": follow_counter,
        }, status=200)
    except:
        new_follow = Follow(follow_user=current_user, follow_following=user_tofollow)
        new_follow.save()
        follow_counter = Follow.objects.filter(follow_following=user_tofollow).count()
        return JsonResponse({
            "message": "User followed.",
            "followers": follow_counter,
        }, status=200)
    
@login_required(login_url='/login', redirect_field_name=None)
def follow_index(request):
    current_user = User.objects.get(pk=request.user.id)
    following_user = Follow.objects.filter(follow_user=current_user)
    posts = []
    for user in following_user:
        user_posts = Post.objects.filter(post_user=user.follow_following) #.order_by("-post_timestamp")
        for post in user_posts:
            try:
                if_liked = Like.objects.get(like_post=post.id, like_by=current_user)
                post.liked_by_user = True
            except:
                post.liked_by_user = False
            posts.append(post)
    all_posts = sorted(posts, key=lambda post: post.post_timestamp, reverse=True)
    if not all_posts:
        return render(request, "network/follow_index.html", {
            "empty": True
        })
    else:
        # Paginate
        page = request.GET.get('page', 1)
        paginator = Paginator(all_posts, 10)
        try:
            posts_pagination = paginator.page(page)
        except PageNotAnInteger:
            posts_pagination = paginator.page(1)
        except EmptyPage:
            posts_pagination = paginator.page(paginator.num_pages)
        return render(request, "network/follow_index.html", {
            "posts": posts_pagination
        })

@login_required(login_url='/login', redirect_field_name=None)
@csrf_exempt
def edit(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        current_user = User.objects.get(pk=request.user.id)
        post = Post.objects.get(pk=id)
        try:
            if_liked = Like.objects.get(like_post=post.id, like_by=current_user)
            liked_by_user = True
        except:
            liked_by_user = False
        try:
            post.post_content = data["edit_content"]
            post.save()
            return JsonResponse({
                "message": "Post edited succesfully.",
                "user": current_user.username,
                "timestamp": post.post_timestamp.strftime("%b %#d %Y, %#I:%M %p"),
                "likes": post.post_likes,
                "liked_by_user": liked_by_user,
                "post_id": post.id,
            }, status=200)
        except:
           return JsonResponse({
                "message": "Error editing post."
            }, status=404)

@login_required(login_url='/login', redirect_field_name=None)
def like(request, id):
    if request.method == "GET":
        current_user = User.objects.get(pk=request.user.id)
        post = Post.objects.get(pk=id)
        try:
            if_liked = Like.objects.get(like_post=post, like_by=current_user)
            if_liked.delete()
        except:
            if_liked = Like(like_post=post, like_by=current_user)
            if_liked.save()
        total_likes = Like.objects.filter(like_post=post).count()
        post.post_likes = total_likes
        post.save()
        return JsonResponse({
            "message": "Post liked.",
            "total_likes": total_likes
        })
