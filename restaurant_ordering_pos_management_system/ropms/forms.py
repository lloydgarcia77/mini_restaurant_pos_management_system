from django import forms
from ropms import models

class CustomerForm(forms.ModelForm):  
    class Meta:
        model = models.Customer
        exclude = ("date_added",)