from django.conf.urls import url
from . import views

app_name="carts"
urlpatterns = [
    url(r'^(?P<cart_id>[0-9]+)/cartindex/$',views.index,name="index"),
    url(r'^(?P<order_id>[0-9]+)/shoplist/$',views.shoplist,name="shoplist" ),
    url(r'^(?P<cart_id>[0-9]+)/validate/$',views.validate_cart,name="validatecart" ),
    url(r'^(?P<cart_id>[0-9]+)/recap/$',views.recap_cart,name="recap" ),
    url(r'^(?P<cart_id>[0-9]+)/addtocart/$',views.add_to_cart,name="addtocart"),
    url(r'^(?P<cart_id>[0-9]+)/(?P<item_id>[0-9]+)/changequantity/$',views.change_quantity,name="changequantity"),
    url(r'^(?P<cart_id>[0-9]+)/(?P<item_id>[0-9]+)/removefromcart/$',views.remove_from_cart,name="removefromcart"),
]
