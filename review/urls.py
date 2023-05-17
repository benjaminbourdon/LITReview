from django.urls import path
from . import views

urlpatterns = [
    path("posts", views.OwnPostsListView.as_view(), name="my_posts"),
    path("abonnements", views.linked_users_view, name="linked_users"),
    path("abonnements/<int:id>/unfollow", views.unfollow_user, name="unfollow"),
    path("tickets", views.TicketCreate.as_view(), name="add_ticket"),
    path("tickets/<int:pk>/edit", views.TicketUpdate.as_view(), name="modify_ticket"),
    # path("tickets/<int:pk>/delete", views.TicketDelete.as_view(), name="delete_ticket"),
]
