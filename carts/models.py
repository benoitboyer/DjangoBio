from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from products.models import Product
from profiles.models import Profile
from django.utils import timezone
from django.template import defaultfilters
import datetime
import decimal


#define your taxes here
#Taxes = TVA + Transport + OM :34%
TAXES = 1.34

# Create your models here.
class Order(models.Model):
	user = models.ManyToManyField(Profile)
	max_date = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=30))
	active = models.BooleanField(default=True)

	def get_all_active_carts(self):
		carts=self.cart_order_set.filter(cart_active=True)
		return carts

	def get_cart_by_user(self,user_id=None):
		cart= self.cart_order_set.filter(cart_user=user_id)
		return cart

	def desactivate_order(self):
		if timezone.now() > self.max_date:
			self.active=False
			self.save()

	def __str__(self):
		return "Order : "+defaultfilters.date(self.max_date,"d/m/Y")


class Cart(models.Model):

	cart_user = models.ForeignKey(Profile, null=True, blank=True)
	cart_order =models.ForeignKey(Order,null=True, blank=True)
	cart_price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	cart_active = models.BooleanField(default=False)

	def __str__(self):
		return "Cart#"+ str(self.id)

	def save(self, *args, **kwargs):
		"""Saves items in cart and re-calculates total price of cart each time"""
		self.calculate_cart_price()
		super(Cart, self).save(*args, **kwargs)

	def get_cart_item(self):
		return self.cartitem_set.all()

	def cart_size(self):
		return len(self.get_cart_item())

	def calculate_cart_price(self):
		total=0
		items = self.get_cart_item()
		for item in items:
			total += item.cart_item_total
		self.cart_price = total

	def activate_cart(self):
		#Put a cart from inactive to active
		self.cart_active = True
		self.save()
	

class CartItem(models.Model):
	cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	cart_item_name = models.CharField(max_length=80, null=True)
	cart_item_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	cart_item_quantity = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "Cart #" + str(self.cart.pk) + " - " + str(self.product)

	def save(self, *args, **kwargs):
		"""Creates cart_item_name attribute if none exists.
		Calculates new cart_item_total on every save
		"""
		if not self.cart_item_name:
			self.cart_itame_name = self.product.product_name
		self.calculate_total()
		super(CartItem, self).save(*args, **kwargs)

	def get_price(self):
		#get price of related product
		return self.product.get_price()

	def get_quantity(self):
		return self.cart_item_quantity

	def calculate_total(self):
		"""Calculates cart_item_total. Called during every save"""	
		self.cart_item_total = round((self.get_quantity() * self.get_price())*decimal.Decimal(TAXES),2)

	def update_quantity(self,quantity):
		#update the cart_item_quantity
		self.cart_item_quantity=quantity
		self.save()
