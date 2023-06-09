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


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update({"class": "link-button"})

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "body": forms.Textarea(),
            "rating": forms.RadioSelect(
                attrs={"class": "input_rate"},
                choices=[(i, f" - {str(i)}") for i in range(0, 5 + 1)],
            ),
        }
