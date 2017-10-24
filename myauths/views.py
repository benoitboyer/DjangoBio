from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import views
from .forms import SignUpForm

class LoginView(views.LoginView):

	template_name= 'myauths/login.html'
	

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'myauths/signup.html', {'form': form})

def logout_view(request):
    # Redirect to a success page.
    logout(request)
    return redirect('home')
