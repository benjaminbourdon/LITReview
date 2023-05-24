from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from review.models import UserFollows
from review.forms import FollowsUserForm


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
