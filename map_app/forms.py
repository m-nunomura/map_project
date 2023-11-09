from .models import AddressList,StoreList
from django import forms

# Create your models here.
class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressList
        fields = ("name","address","category","year","level")



class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreList
        fields = ("name","address")
