from itertools import chain
from typing import Any, Dict

from django.db.models import CharField, Value, Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from review.models import Review, Ticket, UserFollows
from review.forms import FollowsUserForm


class OwnPostsListView(LoginRequiredMixin, generic.ListView):
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
