from django.shortcuts import render,get_object_or_404
from django.http import Http404 
from .models import Cart,CartItem,Order
from .forms import ShopListForm,ChangeQuantityForm
from profiles.models import Profile
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
@login_required

def index(request,cart_id):
	#get the cart
	cart=get_object_or_404(Cart,pk=cart_id)
	#get the order_id and profile of this cart because we don't want other people messing with someone else cart
	cart_profile=cart.cart_user

	if (request.user.id == cart_profile.user.id):
		return render(request,'carts/index.html',{'cart':cart})
	else:
		raise Http404

def validate_cart(request,cart_id):
	cart=get_object_or_404(Cart,pk=cart_id)
	cart.activate_cart()
	cart_profile=cart.cart_user
	if (request.user.id == cart_profile.user.id):
		return render(request,'carts/validate.html',{'cart':cart})
	else:
		raise Http404

def recap_cart(request,cart_id):
	cart=get_object_or_404(Cart,pk=cart_id)
	cart_profile=cart.cart_user
	if (request.user.id == cart_profile.user.id):
		return render(request,'carts/bill.html',{'cart':cart})
	else:
		raise Http404

def view_cart(request):
	"""Not use for now, will show all validate carts for an order"""
	cart=Cart.objects.all()
	return render(request,'carts/index.html',{'carts':cart})

def change_quantity(request,cart_id,item_id):
	"""change the quantity of an item in the cart using ajax call"""
	if request.is_ajax():
		cart=get_object_or_404(Cart,pk=cart_id)
		myForm=ChangeQuantityForm(request.POST)
		if myForm.is_valid():
			quantity= myForm.cleaned_data['quantity']
			cart_item=cart.cartitem_set.get(id=item_id)
			cart_item.cart_item_quantity=quantity
			cart_item.save()
			cart.save()
			from django.forms.models import model_to_dict
			dict_cart = model_to_dict( cart )
			dict_cart_item =model_to_dict(cart_item)

			data={
				'message':'form is saved',
				'cart':dict_cart,
				'cart_item':dict_cart_item,
			}
			return JsonResponse(data)
		else:
			for k,v in myForm.errors.items():
					key=k
					value=v[0]
			data = {
				'err': str(key+" - "+value),
				'item_id':item_id,
			}
			return JsonResponse(data,status=500)
	else:
		raise Http404

def remove_from_cart(request,cart_id,item_id):
	"""remove an item from cart using ajax call"""
	if request.is_ajax():
		cart =get_object_or_404(Cart,pk=cart_id)
		cart_item=cart.cartitem_set.get(id=item_id)
		cart_item.delete()
		cart.save()
		from django.forms.models import model_to_dict
		dict_cart = model_to_dict( cart )
		data = {
			'msg':'item successfully remove from cart',
			'cart':dict_cart,

		}
		return JsonResponse(data)


def add_to_cart(request,cart_id):
	"""add or create a cart_item from product shop list"""
	if request.is_ajax():
		cart=get_object_or_404(Cart,pk=cart_id)
		myform=ShopListForm(request.POST)
		if myform.is_valid():
			#the form is valid,get all the cleaned data
			product_quantity= myform.cleaned_data['quantity']
			product_name= myform.cleaned_data['product_name']
			product_id= myform.cleaned_data['product_id']
			product=get_object_or_404(Product,pk=product_id)

			#get or create  a cart_item for the product to add, 
			#if exist,update the quantity if not create it with the cleaned values
			cart_item, created = CartItem.objects.get_or_create(
				cart = cart,
				product = product,
				defaults  = {'cart_item_name':product_name,'cart_item_quantity':product_quantity}
			)
			if created:
				#the cart_item needs to be save with the value and call for cart save to calculate the price
				cart_item.save()
				cart.save()
			else:
				#cart_item already exists, need to update the name and quantity and make sure the quantity add
				cart_item.cart_item_quantity+=product_quantity
				cart_item.save()
				cart.save()

			from django.forms.models import model_to_dict
			dict_cart = model_to_dict( cart )
			data = {
				'message':'form is saved',
				'cart':dict_cart
			}
			return JsonResponse(data)
		else:

			for k,v in myform.errors.items():
				key=k
				value=v[0]
			data = {
				'err': str(key+" - "+value)
			}
			#data = myform.errors.items();
			return JsonResponse(data,status=500)

def shoplist(request,order_id):
	#test order_id is correct
	order=get_object_or_404(Order,pk=order_id)
	profile =get_object_or_404(Profile,user=request.user)
	#Create a cart if it's not exist yet for the Profile used
	cart, created = Cart.objects.get_or_create(
		cart_user = profile,
		cart_order= order,
		defaults  = {'cart_price':0,'cart_active':False}
		)
	#get all items of the current cart
	cart_items= cart.get_cart_item()
	#get all the products selected by admin 
	shop_items = Product.get_selected_product()
	#render a template for our shoplist
	return render(request,'carts/shoplist.html',{'cart':cart,'cart_items':cart_items,'shop_items':shop_items})