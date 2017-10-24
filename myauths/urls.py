from django.conf.urls import url
from . import views

app_name="myauths"
urlpatterns = [
    url(r'^login/$',views.LoginView.as_view(),name="login" ),
   	url(r'^signup/$',views.signup,name="signup"),
   	url(r'^logout/$',views.logout_view,name="logout" ),
]
