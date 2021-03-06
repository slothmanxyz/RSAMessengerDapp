from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from web3 import Web3

from .forms import SignupForm
from Key.models import Key

#The views and templates in this app are placeholders. Will use the ones in the Pages app instead later.

#Currently deployed to local hardhat network only
provider = Web3.HTTPProvider('http://127.0.0.1:8545/')
web3 = Web3(provider)

# Create your views here.
def home_view(request):
    context={}
    if not request.user.is_authenticated:
        return render(request, 'User/home.html', context)
    else:
        return redirect('dashboard')

def dashboard_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        context['username'] = request.user.username
        context['address'] = request.user.address
        context['balance'] = web3.fromWei(web3.eth.get_balance(request.user.address), 'ether')
        context['keys'] = Key.objects.filter(user=request.user,is_main_key=True)
        return render(request, 'User/dashboard.html', context)

def signup_view(request):
    context = {}
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
        else:
            context['signup_form'] = form
    else:
        form = SignupForm()
        context['signup_form'] = form
    return render(request, 'User/signup.html', context)

def login_view(request):
    context = {}
    if request.POST:
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
        else:
            context['login_form'] = form
    else:
        form = AuthenticationForm()
        context['login_form'] = form 
    return render(request, 'User/login.html', context)

def logout_request(request):
    logout(request)
    return redirect('home')