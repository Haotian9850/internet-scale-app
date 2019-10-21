from django import forms

class ResetPasswordForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))

