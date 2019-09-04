from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    print(request.user)
    if request.user.is_authenticated:
        return render(request, "home.html")
    
    return redirect("login")