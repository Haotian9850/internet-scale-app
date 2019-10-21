from django import forms

class ResetForm(forms.Form):
    new_password = forms.CharField(label="New password", max_length=255, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))

