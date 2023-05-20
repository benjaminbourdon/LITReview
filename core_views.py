from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


class Signup(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = "inscription"
