from typing import Any, Dict
from functools import cached_property

from django.http.response import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from review.models import Review, Ticket


class ReviewCreateFromTicket(
    LoginRequiredMixin, UserPassesTestMixin, generic.edit.CreateView
):
    model = Review
    fields = ["headline", "body", "rating"]
    success_url = reverse_lazy("my_posts")

    title = "Créer une critique"

    permission_denied_message = (
        "Vous n'avez pas l'autorisation de créer une critique"
        + " pour un ticket ayant déja bénéficié d'une critique."
    )
    raise_exception = False

    def test_func(self):
        return not (Review.objects.filter(ticket=self.ticket).exists())

    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            # Ajouter un message d'erreur ?
            return HttpResponseRedirect(reverse_lazy("flux"))
        return super().handle_no_permission()

    @cached_property
    def ticket(self):
        ticket_id = self.kwargs["ticket_id"]
        return Ticket.objects.get(id=ticket_id)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.ticket = self.ticket
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket"] = self.ticket
        context["title"] = self.title
        return context
