from django.contrib import admin

from review.models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user_resume", "time_created")


admin.site.register(Review)
admin.site.register(UserFollows)
