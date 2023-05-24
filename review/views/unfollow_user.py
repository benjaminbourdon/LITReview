from django.db.models import Model
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from review.models import UserFollows


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
