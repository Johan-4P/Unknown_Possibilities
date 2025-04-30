from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'description', 'price', 'stock', 'image', 'category']


    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError("Name cannot be blank or only spaces.")
        return name

    def clean_description(self):
        desc = self.cleaned_data['description']
        if not desc.strip():
            raise forms.ValidationError("Description cannot be blank or only spaces.")
        return desc
    
    def clean_sku(self):
        sku = self.cleaned_data.get('sku', '')
        if not sku.strip():
            raise forms.ValidationError("SKU cannot be blank or just spaces.")
        return sku