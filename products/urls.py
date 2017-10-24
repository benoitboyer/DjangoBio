from django.conf.urls import url
from . import views

app_name="products"
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name="index" ),
    url(r'^searchlist/$',views.search_product_index,name="search_index"),
    url(r'^chooselist/$',views.choose_product,name="choose"),
]
