from django.shortcuts import render,redirect
from .forms import AgregarUsuario, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('gestionUsuario')
    else:
        return redirect('login')

@login_required(login_url='login')
def gestionUsuario(request):
    usuarios=User.objects.all()
    form=AgregarUsuario(request.POST)
    if form.is_valid():
        data=form.cleaned_data
        u=User.objects.create_user(data.get("username"),data.get("correo"),data.get("password"))
        u.save()
    form=AgregarUsuario()
    return render(request,"GestionarUsuario.html",{'form':form,'usuarios':usuarios})

def ingresar(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        user=authenticate(username=data.get("username"),password=data.get("password"))
        if user is not None:
            login(request, user)
            return redirect('gestionUsuario')
    return render(request,"login.html",{'form':form})
def salir(request):
    logout(request)
    return redirect("/")