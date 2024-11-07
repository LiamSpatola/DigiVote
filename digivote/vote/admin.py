from django import forms
from django.contrib import admin
from django.forms import Textarea

from .models import Candidate, Choice, Election, Poll

# Register your models here.
admin.AdminSite.site_header = "DigiVote Administration"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3


class PollAdminForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = "__all__"
        widgets = {
            "voting_instructions": Textarea(attrs={"rows": 5, "cols": 80}),
        }


class ElectionAdminForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = "__all__"
        widgets = {
            "voting_instructions": Textarea(attrs={"rows": 5, "cols": 80}),
        }


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    form = PollAdminForm

    fieldsets = [
        (None, {"fields": ["poll_text"]}),
        ("Date Information", {"fields": ["publish_date", "open_date", "close_date"]}),
        ("Voting Instructions", {"fields": ["voting_instructions"]}),
        ("Visibility", {"fields": ["visible", "results_visible"]}),
    ]
    inlines = [ChoiceInline]

    list_display = (
        "poll_text",
        "publish_date",
        "close_date",
        "poll_open",
        "visible",
        "results_visible",
        "id",
    )
    search_fields = ("poll_text",)
    list_filter = ("publish_date", "poll_open", "results_visible")


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    form = ElectionAdminForm

    fieldsets = [
        (None, {"fields": ["election_name"]}),
        ("Date Information", {"fields": ["publish_date", "open_date", "close_date"]}),
        ("Visibility", {"fields": ["visible", "results_visible"]}),
        ("Voting Instructions", {"fields": ["voting_instructions"]}),
        ("Election Configuration", {"fields": ["election_type", "number_of_seats"]}),
    ]
    inlines = [CandidateInline]

    list_display = (
        "election_name",
        "publish_date",
        "close_date",
        "election_open",
        "election_type",
        "number_of_seats",
        "visible",
        "results_visible",
        "id",
    )
    search_fields = ("election_name",)
    list_filter = ("publish_date", "election_open", "results_visible")
