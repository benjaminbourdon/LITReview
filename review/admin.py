from django.contrib import admin

from review.models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "time_created")
    list_filter = ("user", "time_created")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ["headline", "body", "rating", "ticket", "user"]


admin.site.register(UserFollows)
