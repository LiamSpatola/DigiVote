from django.contrib import admin
from .models import Poll, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["poll_text"]}),
        ("Date information", {"fields": ["publish_date"], "classes": ["collapse"]}),
        ("Poll Status", {"fields": ["poll_open"], "classes": ["collapse"]})
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.AdminSite.site_header = "DigiVote Administration"