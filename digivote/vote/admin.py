from django.contrib import admin

from .models import Choice, Poll

# Register your models here.
admin.AdminSite.site_header = "DigiVote Administration"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["poll_text"]}),
        ("Date Information", {"fields": ["publish_date", "open_date", "close_date"]}),
        ("Visibility", {"fields": ["visible", "results_visible"]}),
    ]
    inlines = [ChoiceInline]

    list_display = (
        "poll_text",
        "publish_date",
        "close_date",
        "poll_open",
        "visible",
        "id",
    )
    search_fields = ("poll_text",)
    list_filter = ("publish_date", "poll_open")
