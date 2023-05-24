from itertools import chain
from typing import Any, Dict
from django.db.models import CharField, Value, Count, Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from review.models import Review, Ticket


class FollowedPostsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "flux"
    template_name = "flux.html"

    title = "Flux"

    def get_queryset(self) -> list[Ticket | Review]:
        current_user = self.request.user

        query_following = current_user.following.select_related("followed_user").all()
        following = [pair.followed_user for pair in query_following]

        # Critique d'une personne suivi, de l'utilisateur connecté
        # ou en réponse à un de ses tickets
        reviews = Review.objects.filter(
            Q(user__in=following) | Q(user=current_user) | Q(ticket__user=current_user)
        )
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        # Tickets d'une personne suivi ou de l'utilisateur connecté
        tickets = Ticket.objects.filter(Q(user__in=following) | Q(user=current_user))
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
        tickets = tickets.annotate(Count("review"))

        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )

        return posts

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context
