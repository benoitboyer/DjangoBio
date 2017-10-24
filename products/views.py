from django.shortcuts import render, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Product
from .forms import SearchForm
# Create your views here.
class IndexView(generic.ListView):

	template_name = 'products/index.html'
	context_object_name = 'product_list'

	def get_queryset(self):
		return Product.objects.filter(product_selected=True).order_by('product_article_code')[:20]

def search_product_index(request):
	template_name= "products/products_index.html"
	context_object_name = 'product_list'

	if request.method == "POST":
		search_form = SearchForm(request.POST)
		if search_form.is_valid():

			if search_form.cleaned_data['product_filter']=="product_name":
				search_filter = search_form.cleaned_data['text_filter']
				product_list = Product.objects.filter(product_name__icontains=search_filter).order_by('product_article_code')[:20]

			if search_form.cleaned_data['product_filter']=="product_brand":
				search_filter = search_form.cleaned_data['text_filter']
				product_list = Product.objects.filter(product_brand__icontains=search_filter).order_by('product_article_code')[:20]

			return render(request, template_name,{context_object_name:product_list, 'form':search_form})

	else:
		search_form= SearchForm()
		product_list = Product.objects.all().order_by('product_article_code')[:20]
		return render(request,template_name,{context_object_name:product_list,'form':search_form})

def choose_product(request):
	 
	 if request.method =="POST":
	 	all_products= Product.objects.all()
	 	chosen_product_list=request.POST.getlist('chosen_product')
	 	for product in all_products:
	 		if str(product.id) in chosen_product_list:
	 			print (chosen_product_list)
	 			product.product_selected = True
	 			product.save()
	 	return HttpResponseRedirect(reverse('products:index'))
	 else:
	 	return HttpResponseRedirect(reverse('products:search_index'))
