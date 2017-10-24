from django import forms


class ShopListForm(forms.Form):
	quantity = forms.IntegerField(required=True,min_value=1,max_value=20)
	product_name = forms.CharField(widget=forms.HiddenInput(),max_length=250)
	product_id = forms.IntegerField(widget=forms.HiddenInput(),min_value=0)
        
class ChangeQuantityForm(forms.Form):
	quantity = forms.IntegerField(required=True,min_value=1,max_value=20)