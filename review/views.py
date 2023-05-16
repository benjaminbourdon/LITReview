from itertools import chain
from typing import Any, Dict

from django.db.models import CharField, Value
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic

from review.models import Review, Ticket


class OwnPostsListView(generic.ListView):
    context_object_name = "my_posts"
    template_name = "list_posts.html"

    def get_queryset(self) -> QuerySet[Any]:
        reviews = Review.objects.filter(user=self.request.user)
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        tickets = Ticket.objects.filter(user=self.request.user)
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )

        return posts

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Mes posts"
        return context


def linked_users_view(request):
    current_user = request.user

    query_following = current_user.following.select_related("followed_user").all()
    following = [pair.followed_user for pair in query_following]

    query_followed_by = current_user.followed_by.select_related("user").all()
    followed_by = [pair.user for pair in query_followed_by]

    return render(
        request,
        "linked_users.html",
        context={
            "following": following,
            "followed_by": followed_by,
        },
    )
