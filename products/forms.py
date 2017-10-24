from django import forms
from .models import Product

class SearchForm(forms.Form):

	method_filter=(('product_name', 'Product name'), ('product_brand','Product Brand'))
	text_filter = forms.CharField(label="Search :",max_length=200,required=False)
	product_filter = forms.ChoiceField(widget=forms.RadioSelect, choices=method_filter)
	
	