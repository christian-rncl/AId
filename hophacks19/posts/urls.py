from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path("all", views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),
]
