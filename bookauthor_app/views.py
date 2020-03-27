from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
    return render(request, 'login.html')

def login(request):
    
    user, errors = User.objects.login_validate(request.POST)
    
    if errors:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['user_id'] = user.id
        return redirect("/weather")
    
def register(request):
    
    errors = User.objects.register_validate(request.POST)
    
    if errors:
        for key,error in errors.items():
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.create(first_name=request.POST['first_name'], 
                            last_name=request.POST['last_name'],
                            email=request.POST['email'],
                            password=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode())
        request.session['user_id'] = user.id
        return redirect("/weather")
    
    
def success(request):
    
    context ={
        'user_id' :request.session['user_id']
    }
    return render(request, 'success.html', context)
