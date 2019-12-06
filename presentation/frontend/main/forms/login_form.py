from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Password", max_length=255, widget=forms.PasswordInput(attrs={'class': "form-control"}))

