from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.OwnPostsListView.as_view(), name="my_posts"),
    path("abonnements/", views.linked_users_view, name="linked_users"),
]
