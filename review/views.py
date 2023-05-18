from itertools import chain
from typing import Any, Dict
from functools import cached_property

from django.db.models import CharField, Value, Model, Count
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse

from review.models import Review, Ticket, UserFollows
from review.forms import FollowsUserForm, TicketCreateForm


class FollowedPostsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "flux"
    template_name = "flux.html"

    title = "Flux"

    def get_queryset(self) -> list[Ticket | Review]:
        current_user = self.request.user

        query_following = current_user.following.select_related("followed_user").all()
        following = [pair.followed_user for pair in query_following]
        following.append(current_user)

        reviews = Review.objects.filter(user__in=following)
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

        tickets = Ticket.objects.filter(user__in=following)
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


class OwnPostsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = "my_posts"
    template_name = "list_posts.html"

    title = "Mes posts"

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


@login_required
def linked_users_view(request):
    current_user = request.user

    if request.method == "POST":
        form = FollowsUserForm(request.POST, user=current_user)
        if form.is_valid():
            new_following = UserFollows(
                user=current_user, followed_user=form.cleaned_data["user_to_follow"]
            )
            new_following.save()
            return HttpResponseRedirect("")
    else:
        form = FollowsUserForm(user=current_user)

    query_following = current_user.following.select_related("followed_user").all()
    following = [pair.followed_user for pair in query_following]

    query_followed_by = current_user.followed_by.select_related("user").all()
    followed_by = [pair.user for pair in query_followed_by]

    return render(
        request,
        "linked_users.html",
        context={
            "form": form,
            "following": following,
            "followed_by": followed_by,
        },
    )


@login_required
def unfollow_user(request, id):
    try:
        userfollows = UserFollows.objects.get(user=request.user, followed_user__id=id)
    except Model.DoesNotExist:
        pass
    else:
        userfollows.delete()
    finally:
        return HttpResponseRedirect(reverse("linked_users"))


class TicketCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Ticket
    fields = ["title", "description"]
    success_url = reverse_lazy("my_posts")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    model = Ticket
    fields = ["title", "description"]
    success_url = reverse_lazy("my_posts")

    def test_func(self):
        # Vérifie que l'utilisateur connecté est bien l'auteur du ticket à modifier
        return self.get_object().user == self.request.user


# class TicketDelete(LoginRequiredMixin, UserPassesTestMixin, generic.edit.DeleteView):
#     model = Ticket
#     success_url = reverse_lazy("my_posts")

#     def test_func(self):
#         # Vérifie que l'utilisateur connecté est bien l'auteur du ticket à supprimer
#         return self.get_object().user == self.request.user


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


class ReviewCreateWithNewTicket(LoginRequiredMixin, generic.edit.CreateView):
    model = Review
    fields = ["headline", "body", "rating"]
    success_url = reverse_lazy("my_posts")

    title = "Créer une critique"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ticket_form"] = TicketCreateForm(self.request.POST)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ticket_form = TicketCreateForm(self.request.POST)
        ticket_form.instance.user = self.request.user
        if ticket_form.is_valid():
            new_ticket = ticket_form.save()

        form.instance.ticket = new_ticket
        form.instance.user = self.request.user
        return super().form_valid(form)
