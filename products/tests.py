from django.test import TestCase
from django.urls import reverse
from .models import Product
from .forms import SearchForm

# Create your tests here.

"""Function for create a Product for many tests"""
def CreateProduct(product_name,bool_product_selected):
	return Product.objects.create(product_name=product_name,product_selected=bool_product_selected,product_code=1,product_price=1)

class ModelProductTests(TestCase):

	def test_product_was_selected_by_default(self):
		"""Return False by default"""
		product_test=Product(product_name="Test")
		self.assertIs(product_test.product_was_selected(),False)

	def test_product_was_selected_with_false(self):
		"""Return False if product_selected = False"""
		product_test=Product(product_name="Test", product_selected=False)
		self.assertIs(product_test.product_was_selected(),False)

	def test_product_was_selected_with_true(self):
		"""Return True if product_selected = True"""
		product_test=Product(product_name="Test", product_selected=True)
		self.assertIs(product_test.product_was_selected(),True)

class ProductIndexViewTests(TestCase):

	def test_indexview_with_no_product(self):
		"""Return a status code 200
		response that contains "No availlable products" and an empty context"""
		response=self.client.get(reverse('products:index'))
		self.assertEqual(response.status_code,200)
		self.assertQuerysetEqual(response.context['product_list'],[])
		self.assertContains(response,"No availlable products")

	def test_indexview_with_no_selected_product(self):
		"""Return a status code 200
		response that contains "No availlable products" and an empty context"""
		product_test=CreateProduct("Test",False)
		response=self.client.get(reverse('products:index'))
		self.assertEqual(response.status_code,200)
		self.assertQuerysetEqual(response.context['product_list'],[])
		self.assertContains(response,"No availlable products")

	def test_indexview_with_one_selected_product(self):
		"""Return a product_list in the context"""
		product_test=CreateProduct("Test",True)
		response=self.client.get(reverse('products:index'))
		self.assertQuerysetEqual(response.context['product_list'],['<Product: Test>'])
		
	def test_indewview_with_multiple_selected_product(self):
		"""Return a product_list order_by product_article_code"""
		product_test_one=CreateProduct("Sunflower seeds",True)
		product_test_one.product_article_code="Sun01"
		product_test_one.save()

		product_test_two=CreateProduct("Almond juce",True)
		product_test_two.product_article_code="Alm01"
		product_test_two.save()

		response=self.client.get(reverse('products:index'))
		self.assertQuerysetEqual(response.context['product_list'],['<Product: Almond juce>','<Product: Sunflower seeds>'])
		
	def test_indexview_with_multiple_selected_and_unselected_products(self):
		"""Return only the selected products order by produt_article_code"""
		product_test_one=CreateProduct("Sunflower seeds",True)
		product_test_one.product_article_code="Sun01"
		product_test_one.save()

		product_test_two=CreateProduct("Almond juce",True)
		product_test_two.product_article_code="Alm01"
		product_test_two.save()

		product_test_three=CreateProduct("Mango",False)
		product_test_three.product_article_code="Man01"
		product_test_three.save()

		product_test_four=CreateProduct("Cardamone seeds",False)
		product_test_four.product_article_code="Car01"
		product_test_four.save()

		response=self.client.get(reverse('products:index'))
		self.assertQuerysetEqual(response.context['product_list'],['<Product: Almond juce>','<Product: Sunflower seeds>'])

class SearchProductIndexTest(TestCase):

	def test_with_no_product(self):
		"""REturn status code 200, contains "No availlable products, context[]=[]"""
		response=self.client.get(reverse('products:search_index'))
		self.assertIs(response.status_code,200)
		self.assertContains(response,"No availlable products")
		self.assertQuerysetEqual(response.context['product_list'],[])

	def test_with_one_product(self):
		 """REturn response.context['product_list']=['<Product: test1>']"""
		 test_product=CreateProduct("test1",True)
		 response=self.client.get(reverse('products:search_index'))
		 self.assertQuerysetEqual(response.context['product_list'],['<Product: test1>'])

	def test_with_multiple_product(self):
		"""REturn a list of the two products order by article_code"""
		test_product1=CreateProduct("test1",True)
		test_product1.article_code="tes01"
		test_product2=CreateProduct("test2",True)
		test_product2.article_code="tes02"

		response=self.client.get(reverse('products:search_index'))
		self.assertQuerysetEqual(response.context['product_list'],['<Product: test1>','<Product: test2>'])

	