from django.shortcuts import render,redirect
from .forms import AgregarUsuario, LoginForm, RestablecerPassForm
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

#Gestion de Usuarios
def gestionUsuario(request):
    usuarios=User.objects.all()
    form=AgregarUsuario(request.POST)
    if form.is_valid():
        data=form.cleaned_data
        u=User.objects.create_user(data.get("username"),data.get("correo"),data.get("password"))
        u.save()
    form=AgregarUsuario()
    return render(request,"GestionarUsuario.html",{'form':form,'usuarios':usuarios})
#Vista del Login
def ingresar(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        user=authenticate(username=data.get("username"),password=data.get("password"))
        if user is not None:
            login(request, user)
            return redirect('gestionUsuario')
    return render(request,"login.html",{'form':form})

#Salir
def salir(request):
    logout(request)
    return redirect("/")

# Recuperacion Contraseña
def recovery(request):
    form=RestablecerPassForm(request.POST or None)
    mensaje=""
    if form.is_valid():
        data=form.cleaned_data
        user=User.objects.get(username=data.get("username"))
        send_mail(
                'Recuperación de contraseña',
                'Haga click aquí para ingresar una nueva contraseña',
                [user.email],
                html_message = 'Pulse <a href="http://localhost:8000/restablecer?user='+user.username+'">aquí</a> para restablecer su contraseña.',
            )
        mensaje='Correo Enviado a '+user.email
    return render(request,"passwdrcv.html",{'form':form, 'mensaje':mensaje})
