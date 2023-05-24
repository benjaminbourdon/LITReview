from django.db.models import Model
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from review.models import Ticket


@login_required
def delete_ticket(request, pk: int):
    try:
        ticket = Ticket.objects.get(id=pk)
    except Model.DoesNotExist:
        pass
    else:
        if ticket.user == request.user:
            ticket.delete()
    finally:
        return HttpResponseRedirect(reverse("my_posts"))
