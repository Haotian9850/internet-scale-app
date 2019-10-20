from django import forms 

class CreatePetForm(forms.Form):
    name = forms.CharField(label="Pet name", widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    pet_type = forms.CharField(label="Pet type", widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    description = forms.CharField(label="Pet description", widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))
    price = forms.DecimalField(label="Price(USD)", min_value=0, decimal_places=2, widget=forms.TextInput(attrs={'class': "form-field form-control col-sm-10"}))