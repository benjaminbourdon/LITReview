from django import forms
from django.contrib.auth import get_user_model

from review.models import Review, Ticket


class FollowsUserForm(forms.Form):
    user_to_follow = forms.ModelChoiceField(
        queryset=None,
        empty_label="(Nom d'utilisateur)",
        label="",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        already_follow = self.user.following.select_related("followed_user")
        already_follow = already_follow.values("followed_user")

        User = get_user_model()
        queryset = User.objects.exclude(id__in=already_follow).exclude(id=self.user.id)

        self.fields["user_to_follow"].queryset = queryset


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
