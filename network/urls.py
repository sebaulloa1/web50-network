
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("user/<int:id>", views.user, name="user"),
    path("follow_index", views.follow_index, name="follow_index"),
    

    # API
    path("new_post", views.new_post, name="new_post"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like"),
]
