from django import forms


class LogInForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))