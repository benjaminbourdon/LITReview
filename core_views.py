from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView


class Signup(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "inscription"


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("my_posts"))
    else:
        return HttpResponseRedirect(reverse("login"))
