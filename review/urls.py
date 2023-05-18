from django.urls import path
from . import views

urlpatterns = [
    path("flux", views.FollowedPostsListView.as_view(), name="flux"),
    path("posts", views.OwnPostsListView.as_view(), name="my_posts"),
    path("abonnements", views.linked_users_view, name="linked_users"),
    path("abonnements/<int:id>/unfollow", views.unfollow_user, name="unfollow"),
    path("tickets", views.TicketCreate.as_view(), name="add_ticket"),
    path("tickets/<int:pk>/edit", views.TicketUpdate.as_view(), name="modify_ticket"),
    # path("tickets/<int:pk>/supprimer", views., name="delete_ticket"),
    path(
        "tickets/<int:ticket_id>/critique",
        views.ReviewCreateFromTicket.as_view(),
        name="review_for_ticket",
    ),
    path("critiques", views.ReviewCreateWithNewTicket.as_view(), name="fresh_review"),
    # path("critiques/<int:pk>/edit", views., name="modify_review"),
]
