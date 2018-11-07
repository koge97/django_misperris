from django.shortcuts import render,redirect
from .forms import AgregarUsuario, LoginForm, RestablecerPassForm, RestablecerPassMail
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

#Index
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
#Login
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

#Enviar Mail para cambiar contraseña
def recovery(request):
    form=RestablecerPassMail(request.POST or None)
    confirmacion="hola soy un relleno owo"
    if form.is_valid():
        data=form.cleaned_data
        user=User.objects.get(username=data.get("username"))
        send_mail(
                'Recuperación de contraseña',
                'Haga click aquí para ingresar una nueva contraseña',
                'from@example.com',
                [user.email],
                html_message = 'Pulse <a href="http://localhost:8000/changepassword?user='+user.username+'">aquí</a> para restablecer su contraseña.',
            )
        confirmacion='Se enviaron las instrucciones para restablecer la contraseña a '+user.email
    return render(request,"passwdrcv.html",{'form':form, 'confirmacion':confirmacion})

#Restablecer Contraseña
def changepassword(request):
    form=RestablecerPassForm(request.POST or None)
    msgbox=""
    try:
        username=request.GET["user"]
    except Exception as e:
        username= None
    if username is not None:
        if form.is_valid():
            data=form.cleaned_data
            if data.get("nuevapass") == data.get("nuevapasscheck"):
                passwd=make_password(data.get("nuevapasscheck"))
                User.objects.filter(username=username).update(password=passwd)
                msgbox="Contraseña cambiada exitosamente"
            else:
                msgbox="Las contraseñas deben coincidir, intentelo de nuevo"
        return render(request,"changepassword.html",{'form':form, 'username':username, 'msgbox':msgbox})
    else:
        return redirect('/login/')