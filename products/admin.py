from django.contrib import admin
from .models import Product
# Register your models here.


class MyProduct(Product):
    class Meta:
        proxy = True

class MyProductAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        return self.model.objects.filter(product_selected = True)

    def unselect_product(MyProductAdmin,request,queryset):
    	for obj in queryset:
    		obj.product_selected=False
    		obj.save()
    
   
    unselect_product.short_description = "Mark products will be unselected"
    actions = [unselect_product]

admin.site.register(Product)
admin.site.register(MyProduct, MyProductAdmin)