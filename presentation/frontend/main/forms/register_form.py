from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=255, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    first_name = forms.CharField(label="First name", max_length=255, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    last_name = forms.CharField(label="Last name", max_length=255, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    age = forms.IntegerField(label="Age", min_value=0, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    gender = forms.ChoiceField(label="Gender", choices=[("1", "None"), ("2", "Female"), ("3", "Male"), ("4", "Other")], widget=forms.Select(attrs={'class': "form-dropdown"}))
    email_address = forms.EmailField(label="Email address", widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    zipcode = forms.IntegerField(label="Zipcode", widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    password = forms.CharField(label="Password", max_length=255, widget=forms.PasswordInput(attrs={'class': "form-field form-control col-sm-10"}))
    confirm_password = forms.CharField(label="Confirm Password", max_length=255, widget=forms.PasswordInput(attrs={'class': "form-field form-control col-sm-10"}))
    
   