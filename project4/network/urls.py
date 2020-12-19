
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.post, name="newpost"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow_action/<str:name>", views.follow_action, name="follow_action"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like_action, name="like_action"),
]
