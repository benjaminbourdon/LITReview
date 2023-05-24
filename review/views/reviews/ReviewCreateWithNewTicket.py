from typing import Any, Dict
from functools import cached_property

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from review.models import Review
from review.forms import TicketCreateForm


class ReviewCreateWithNewTicket(LoginRequiredMixin, generic.edit.CreateView):
    model = Review
    fields = ["headline", "body", "rating"]
    success_url = reverse_lazy("my_posts")

    title = "Créer une critique"

    @cached_property
    def ticket_form(self):
        if self.request.POST:
            ticket_form = TicketCreateForm(self.request.POST)
        else:
            ticket_form = TicketCreateForm()
        ticket_form.instance.user = self.request.user
        return ticket_form

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_form"] = self.ticket_form
        context["title"] = self.title
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if self.ticket_form.is_valid():
            new_ticket = self.ticket_form.save()

            form.instance.ticket = new_ticket
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
