from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255),
    first_name = forms.CharField(label="First name", max_length=255),
    last_name = forms.CharField(label="Last name", max_length=255),
    age = forms.IntegerField(label="Age"),
    gender = forms.CharField(label="Gender", max_length=128),
    email_address = forms.EmailField(label="Email address"),
    zipcode = forms.IntegerField(label="Zipcode"),
    password = forms.CharField(label="Password", max_length=255)