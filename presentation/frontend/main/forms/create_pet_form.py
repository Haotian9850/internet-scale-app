from django import forms 

class CreatePetForm(forms.Form):
    name = forms.CharField(label="Pet name")
    pet_type = forms.CharField(label="Pet type")
    description = forms.CharField(label="Pet description")
    price = forms.IntegerField(label="Price")