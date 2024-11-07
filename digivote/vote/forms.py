from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Candidate


class LogInForm(forms.Form):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control mb-3"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"})
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class ElectionVote(forms.Form):
    def __init__(self, *args, candidates=None, **kwargs):
        super(ElectionVote, self).__init__(*args, **kwargs)
        if candidates:
            for i in range(len(candidates)):
                choices = [(None, "Preference")]
                for candidate in candidates:
                    choice_label = (
                        f"{candidate.full_name} ({candidate.affiliation})"
                        if candidate.affiliation
                        else candidate.full_name
                    )
                    choices.append((candidate.id, choice_label))

                self.fields[f"rank_{i+1}"] = forms.ChoiceField(
                    choices=choices,
                    label=f"Preference {i+1}",
                    widget=forms.Select(attrs={"class": "form-control"}),
                    required=True,
                )

    def clean(self):
        cleaned_data = super().clean()
        ranks = []
        for field in self.fields:
            rank = cleaned_data.get(field)
            if rank in ranks:
                self.add_error(field, "Each candidate must be assigned a unique rank.")
            ranks.append(rank)
        return cleaned_data
