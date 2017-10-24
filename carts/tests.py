from django.test import TestCase
from .models import Cart, CartItem
from products.models import Product
from django.shortcuts import reverse
import decimal

"""This is create shortcut function"""
def create_product(product_name,product_price,product_code):
	product= Product.objects.create(product_name=product_name,product_price=product_price,product_code=product_code)
	return product

def create_cart(cart_price,cart_active=False):
	cart=Cart.objects.create(cart_price=cart_price,cart_active=cart_active)
	return cart

def create_cart_item(cart,product,quantity=1):
	cart_item = CartItem.objects.create(cart=cart,product=product,cart_item_quantity=quantity)
	return cart_item


# Create your tests here.
class CartModelTests(TestCase):

    def test__str__(self):
    	"""return the id of the cart"""
    	cart=create_cart(0,True)
    	self.assertEqual(str(cart),"Cart#"+str(cart.id))

    def test_get_cart_item(self):
    	"""return list of cart_item"""
    	cart=create_cart(0,True)
    	product_1= create_product("test 1",12.68,0)
    	product_2= create_product("test 2",10.00,1)
    	cart_item_1=create_cart_item(cart ,product_1)
    	cart_item_2=create_cart_item(cart ,product_2)
    	cart_items= cart.get_cart_item()
    	self.assertEqual(len(cart_items),2)
    	self.assertEqual(list(cart_items),[cart_item_1,cart_item_2])
    	
    def test_cart_size(self):
    	#Return lenght of cart (how many cart items)
    	cart=create_cart(0,True)
    	product_1= create_product("test 1",12.68,0)
    	product_2= create_product("test 2",10.00,1)
    	cart_item_1=create_cart_item(cart ,product_1)
    	cart_item_2=create_cart_item(cart ,product_2)
    	cart_items= cart.get_cart_item()
    	cart_size=cart.cart_size()
    	self.assertEqual(cart_size,2)

    def test_calculate_cart_price(self):
    	#calculate the cart total price and put it in cart_price
    	cart=create_cart(0,True)
    	product_1= create_product("test 1",12.68,0)
    	product_2= create_product("test 2",10.00,1)
    	cart_item_1=create_cart_item(cart ,product_1)
    	cart_item_2=create_cart_item(cart ,product_2)
    	cart.calculate_cart_price()
    	total=(12.68*1.34)+(10*1.34)
    	decimal_total=decimal.Decimal(str(total)).quantize(decimal.Decimal('0.01'))
    	self.assertEqual(cart.cart_price,decimal_total)

    def test_activate_cart(self):
    	"""put cart_active to True"""
    	cart=create_cart(0,False)
    	cart.activate_cart()
    	self.assertIs(cart.cart_active,True)

    def test_save(self):
    	"""test that the overload save method calculate the total cart_price and all our fields are ok"""
    	cart=create_cart(0,False)
    	product_1= create_product("test 1",12.68,0)
    	product_2= create_product("test 2",10.00,1)
    	cart_item_1=create_cart_item(cart ,product_1)
    	cart_item_2=create_cart_item(cart ,product_2)

    	total=(12.68*1.34)+(10*1.34)
    	decimal_total=decimal.Decimal(str(total)).quantize(decimal.Decimal('0.01'))

    	cart.cart_active=True

    	cart.save()
    	self.assertEqual(cart.cart_price,decimal_total)
    	self.assertIs(cart.cart_active,True)

class CartItemModelTests(TestCase):
	pass
