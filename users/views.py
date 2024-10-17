from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,Userform
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
               login(request,user)
               messages.success(request,f'you are logged in as{username} ')
               return redirect('main')
            else:
               pass
               messages.error(request,f'unable to login')
        else:
               messages.error(request,f'unable to login')    
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request,'views/login.html',{'login_form':login_form})

class Registerview(View):
    def get(self, request):
        return render(request, 'views/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email=request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'views/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'views/register.html')

        user = User.objects.create_user(username=username, password=password1,email=email)
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, f'User {user.username} registered successfully.')
            return redirect('main')
        else:
            messages.error(request, 'Unable to register. Please try again.')
            return render(request, 'views/register.html')
        