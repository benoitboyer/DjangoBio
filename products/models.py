from django.db import models

# Create your models here.
class Product(models.Model):
	product_brand = models.CharField(max_length=50)
	product_article_code = models.CharField(max_length=20)
	product_code= models.IntegerField()
	product_name= models.CharField(max_length=150)
	product_unit_packaging_number = models.IntegerField(default=1)
	product_price = models.DecimalField(max_digits=8,decimal_places=2)
	product_selected = models.BooleanField(default=False)

	def __str__(self):
		return self.product_name

	def product_was_selected(self):
		return self.product_selected
	
	def get_price(self):
		return self.product_price		

	def get_selected_product():
		return Product.objects.filter(product_selected=True)
