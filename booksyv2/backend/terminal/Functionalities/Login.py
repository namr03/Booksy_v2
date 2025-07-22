from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

#Those are registration, login and logout functions
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'terminal.backends.EmailBackend'
            login(request,user)
            messages.success(request,"Registration succesful")
            return redirect('home')
        else:
            messages.error(request,"Registration Failed")
    else:
        form = UserRegistrationForm()
    return render(request, 'terminal/register.html',{'form': form})

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            if user.is_superuser:
                login(request,user)
                messages.success(request,'Login successfull as employee')
                return redirect('calendar')
            else:    
                login(request,user)
                messages.success(request,'Login successfull')
                return redirect('home')
        else:
            messages.error(request,"Invalid email or password")
    return render(request,'terminal/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out succesfully')
    return redirect('login')