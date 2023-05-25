# Inspired by https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from review.forms import ReviewCreateForm, TicketCreateForm


@login_required
@transaction.atomic
def review_and_ticket_create(request):
    if request.method == "POST":
        ticket_form = TicketCreateForm(request.POST)
        review_form = ReviewCreateForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket_form.instance.user = request.user
            ticket_form.full_clean()
            ticket = ticket_form.save()
            ticket.refresh_from_db()

            review_form.instance.ticket = ticket
            review_form.instance.user = request.user
            review_form.full_clean()
            review_form.save()
            return HttpResponseRedirect(reverse("my_posts"))
    else:
        ticket_form = TicketCreateForm()
        review_form = ReviewCreateForm()
    return render(
        request,
        "review/review_form.html",
        {
            "ticket_form": ticket_form,
            "form": review_form,
            "title": "Créer une critique",
        },
    )
