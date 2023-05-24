from django.db.models import Model
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from review.models import Review


@login_required
def delete_review(request, pk: int):
    try:
        review = Review.objects.get(id=pk)
    except Model.DoesNotExist:
        pass
    else:
        if review.user == request.user:
            review.delete()
    finally:
        return HttpResponseRedirect(reverse("my_posts"))
