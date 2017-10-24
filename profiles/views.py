from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from carts.models import Order
from .models import Profile
# Create your views here.
@login_required
def index(request):
	current_user = request.user
	try:
		current_user_profile = Profile.objects.get(user=current_user.id)
	except (KeyError, Profile.DoesNotExist):
		return render(request, 'profiles/index.html', {'error_message':'Your profile is not created propely'})

	available_order = Order.objects.filter(active=True)
	your_past_order = current_user_profile.order_set.filter(active=False)

	context= {'available_orders' : available_order,'past_orders':your_past_order}

	return render(request,'profiles/index.html',context)



