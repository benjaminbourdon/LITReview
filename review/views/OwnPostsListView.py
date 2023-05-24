from itertools import chain
from typing import Any, Dict

from django.db.models import CharField, Value
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from review.models import Review, Ticket


class OwnPostsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "my_posts"
    template_name = "list_posts.html"

    title = "Vos posts"

    def get_queryset(self) -> list[Ticket | Review]:
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
        context["title"] = self.title
        return context
