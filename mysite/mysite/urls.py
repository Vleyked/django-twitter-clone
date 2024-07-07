from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/add_comment/", views.add_comment, name="add_comment"),
    path("post/<int:pk>/add_like/", views.add_like, name="add_like"),
    path("add_post/", views.add_post, name="add_post"),
    path("accounts/", include("allauth.urls")),
]
