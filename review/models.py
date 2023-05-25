from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from review.utils import image_upload_path


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="description"
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True, verbose_name="image", upload_to=image_upload_path
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"#{self.id} {self.title}"

    def user_resume(self):
        return f"{self.user.username} <{self.user.email}>"

    user_resume.short_description = "User"

    class Meta:
        ordering = ["-time_created"]


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="note",
    )
    headline = models.CharField(max_length=128, verbose_name="titre")
    body = models.CharField(max_length=8192, blank=True, verbose_name="commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"#{self.id} {self.headline}"

    class Meta:
        ordering = ["-time_created"]


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    def __str__(self) -> str:
        return f"{self.user.username} follows {self.followed_user.username}"

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )
        ordering = ["user__username"]
        verbose_name = "FollowersPair"
