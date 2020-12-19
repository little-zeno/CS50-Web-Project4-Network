import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import User, Post, Follow, Comments
from .forms import NewPostForm, LikeForm

@login_required(login_url = '/login')
def home(request):
    all_post = Post.objects.all()
    paginator = Paginator(all_post, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked = Post.objects.filter(likes = request.user)

    # if 'post_id' in request.POST:
    #     post_id = request.POST.get('post_id')
    #     print(post_id)
    #     current_post = Post.objects.get(id=post_id)
    #     user_in_like = request.user in current_post.likes.all()
    #     print(current_post.likes.all())
    #     if user_in_like:
    #         current_post.likes.remove(request.user)
    #         return HttpResponseRedirect(reverse("home"))
    #     else:
    #         current_post.likes.add(request.user)
    #         return HttpResponseRedirect(reverse("home"))
    
    return render(request, "network/home.html", {"page_obj": page_obj, "liked":liked})


@login_required(login_url = '/login')
def post(request):
    if request.method == "POST":
        new_form = NewPostForm(request.POST)
        if new_form.is_valid():
            new_post = new_form.cleaned_data["post_text"]
            add_post = Post(author=request.user, post_text=new_post).save()
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/newpost.html", {"form": new_form})
    else:
        return render(request, "network/newpost.html", {"form": NewPostForm()})

@login_required(login_url = '/login')
def profile(request, name):
   
    profile_user = User.objects.get(username = name)
    profile_user_id = profile_user.id
    profile_user_posts = Post.objects.filter(author = profile_user_id)

    paginator = Paginator(profile_user_posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profile_following = Follow.objects.get(user = profile_user_id).follow_person.all()
    profile_followers = Follow.objects.get(user = profile_user_id).followed.all()
    
    # Check if logged in user is in profile user's followed list
    follow_check = request.user in profile_followers
    
    # Like function
    liked = Post.objects.filter(likes = request.user)
    # if 'post_id' in request.POST:
    #     post_id = request.POST.get('post_id')
    #     print(post_id)
    #     current_post = Post.objects.get(id=post_id)
    #     # post_author = current_post.author
    #     user_in_like = request.user in current_post.likes.all()
    #     print(current_post.likes.all())
    #     if user_in_like:
    #         current_post.likes.remove(request.user)
    #         return HttpResponseRedirect(reverse("profile", args=[name]))
    #     else:
    #         current_post.likes.add(request.user)
    #         return HttpResponseRedirect(reverse("profile", args=[name]))    
    return render(request, "network/profile.html", {"page_obj": page_obj, "following":profile_following, "followers": profile_followers, "liked": liked, "profile_user": profile_user, "logged_in_user": request.user, "follow_check": follow_check})


@login_required(login_url = '/login')
def follow_action(request, name):

    profile_user = User.objects.get(username = name)
    profile_user_id = profile_user.id
    profile_follow_status = Follow.objects.get(user = profile_user_id)
    
    # Check if logged in user is in profile user's followed list
    follow_check = request.user in profile_follow_status.followed.all()

    # Check if request.user is one of the followers
    if not follow_check:
        profile_follow_status.followed.add(request.user)
        Follow.objects.get(user = request.user.id).follow_person.add(profile_user)
    else:
        profile_follow_status.followed.remove(request.user)
        Follow.objects.get(user = request.user.id).follow_person.remove(profile_user)
    return HttpResponseRedirect(reverse("profile", args=[name]))
    
    
@csrf_exempt
def edit(request, post_id):
    edit_post = Post.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post_text") is not None:
            edit_post.post_text = data["post_text"]
        edit_post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like_action(request, post_id):
    post = Post.objects.get(id = post_id)
    user_in_like = request.user in post.likes.all()

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            if user_in_like:
                post.likes.remove(request.user)
                post.save()
            else:
                post.likes.add(request.user)
                post.save()
    return JsonResponse(post.serialize())
  
@login_required(login_url = '/login')
def following(request):
    all_followings = Follow.objects.get(user = request.user.id).follow_person.all()
    print(all_followings)
    all_followings_posts = Post.objects.filter(author__in = all_followings)
    paginator = Paginator(all_followings_posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked = Post.objects.filter(likes = request.user)
    
    return render(request, "network/home.html", {"page_obj": page_obj, "liked":liked})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "network/register.html")
