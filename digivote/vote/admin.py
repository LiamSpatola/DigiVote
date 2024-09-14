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
        ("Date information", {"fields": ["publish_date"], "classes": ["collapse"]}),
        ("Poll Status", {"fields": ["poll_open"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ("poll_text", "publish_date", "poll_open")
    search_fields = ("poll_text",)
    list_filter = ("publish_date", "poll_open")
