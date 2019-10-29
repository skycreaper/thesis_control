from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def login(request):
    form = AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)    
        print('request...')
        print('data: ', request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                return redirect('home')
        else:
            print("login errors: ", form.errors)
    return render(request, "registration/login.html", {'form':form})


def logout(request):
    do_logout(request)
    return redirect("login")