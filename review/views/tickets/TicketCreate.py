from typing import Any, Dict

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from review.models import Ticket


class TicketCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Ticket
    fields = ["title", "description", "image"]
    success_url = reverse_lazy("my_posts")

    title = "Créer un ticket"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context
