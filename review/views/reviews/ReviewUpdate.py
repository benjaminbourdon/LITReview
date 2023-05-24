from typing import Any, Dict

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from review.models import Review


class ReviewUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    model = Review
    fields = ["headline", "body", "rating"]
    success_url = reverse_lazy("my_posts")

    title = "Modifier votre critique"

    def test_func(self):
        # Vérifie que l'utilisateur connecté est bien l'auteur de la critique à modifier
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["ticket"] = self.get_object().ticket
        return context
