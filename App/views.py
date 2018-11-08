#Importa los formularios AgregarUsuario, LoginForm, RestablecerPassForm, RestablecerPassMail
from .forms import AgregarUsuario, LoginForm, RestablecerPassForm, RestablecerPassMail
#Importa los templates
from django import template
#Importa las respuestas Http
from django.http import HttpResponse
#Importa el render de pagina y la redireccion
from django.shortcuts import render,redirect
#Librerias necesarias para enviar el email
from django.core.mail import send_mail
from django.template.loader import get_template
#Importa la libreria para recuperar el nombre de usuario
from django.contrib.auth.models import User
#Importa la autenticacion, login, etc
from django.contrib.auth import authenticate, login, logout
#Sirve para exigir estar logeado en ciertos sitios
from django.contrib.auth.decorators import login_required
#Convierte el Password de la persona en un Hash SHA256 por default
from django.contrib.auth.hashers import make_password
from .models import Usuario

# Aguante StackOverflow
# Create your views here.

#----------------------------------------------------------------------------------------------------------------------


#Index
def index(request):
    pantalla=get_template("index.html")
    contexto={'titulo':"Index",}
    return HttpResponse(pantalla.render(contexto,request))

#----------------------------------------------------------------------------------------------------------------------

#Gestion de Usuarios desde Admin
def gestionUsuario(request):
    usuarios=User.objects.all()
    form=AgregarUsuario(request.POST)
    if form.is_valid():
        data=form.cleaned_data
        #Aqui va a crear el usuario con los tres parametros principales
        u=User.objects.create_user(data.get("username"),data.get("correo"),data.get("password"))
        #define la variable var_rol como lo que tenga el rol
        var_rol = data.get("rol")
        #Si el rol es normal pues la cuenta que este creando no es staff/admin/superusuario o como le digas
        if var_rol == "Normal":
            u.is_staff=False
            #Si es cualquier otra cosa (Que solo puede ser admin asdasjdasd) sera staff
        else:
            u.is_staff=True
            #Aqui guarda el usuario
        u.save()
        #Aqui obtiene el resto de datos para meterlos en la tabla usuario
        regDB=Usuario(nombre=data.get("nombre"),apellido=data.get("apellido"),fecha=data.get("fecha"),region=data.get("region"),ciudad=data.get("ciudad"),vivienda=data.get("vivienda"),rol=data.get("rol"),user=u)
        #Y aqui los guarda c:
        regDB.save()
    form=AgregarUsuario()
    return render(request,"GestionarUsuario.html",{'form':form,'usuarios':usuarios})
#NOTA: Despues de lesear como 2 horas por que no me tomaba la tabla Usuario, solo habia que hacer un > python manage.py migrate --run-syncdb

#----------------------------------------------------------------------------------------------------------------------

#Login
def ingresar(request):
    #Bueno, en esta parte le esta diciendo que pesque el LoginForm
    form=LoginForm(request.POST or None)
    #Si el form es valido va a hacer...
    if form.is_valid():
        data=form.cleaned_data
        #Va a autenticar los valores de usr y passwd y si no pos nada por que no hay un else xd
        user=authenticate(username=data.get("usr"),password=data.get("passwd"))
        if user is not None:
            login(request, user)
            return redirect('gestionUsuario')
    return render(request,"login.html",{'form':form})

#----------------------------------------------------------------------------------------------------------------------

#Salir
def salir(request):
    #Creo que es algo logico lo que hace no? bueno, sin no se entiende, hace el request del logout
    logout(request)
    #Esto tambien es logico pero de todas formas, te manda al inicio de la pagina despues de deslogear
    return redirect("/")

#----------------------------------------------------------------------------------------------------------------------

#Enviar Mail para cambiar contraseña
def recovery(request):
    form=RestablecerPassMail(request.POST or None)
    #Horas buscando por quer me daba error la variable del mensaje de confirmacion y tenia que meterle algun relleno :/
    confirmacion="hola soy un relleno owo"
    #Si el formulario es valido hace el get del username y manda un sensual correo a la direccion que tenga guardada esta cosa a travez del send_mail
    #Estuve hasta las 4AM tratando de hacer que funcionara y despues me di cuenta que tenia mal escrito el snmp de Google pal Gmail :D (De hecho creo que lo escribi mal de nuevo xd)
    if form.is_valid():
        data=form.cleaned_data
        user=User.objects.get(username=data.get("username"))
        send_mail(
                'Recuperación de contraseña',
                #Why not? Sus escuadrones del Fortnite? Lobuno? Ok no.
                'Me gusta el Fortnite lo juego todo el dia esto no es Minecraft me encanta es muy bueno',
                #Aguanten las Guias de Django y StackOverflow, no se que hace esto pero funciona.
                'from@example.com',
                #Esto pide el mail con el que el usuario se registro
                [user.email],
                #Y aqui va el mensaje, que maravilla verdad?
                html_message = 'Pulse <a href="http://localhost:8000/changepassword?user='+user.username+'">aquí</a> para restablecer su contraseña.',
            )
            #Y aqui va la confirmacion, super magica
        confirmacion='Se enviaron las instrucciones para restablecer la contraseña a '+user.email
        #Si todo sale ok te devuelve al formulario pero con el mensaje de arriba confirmado que se envio el mail, si no, pues anda a rezarle a la virgencita que algo pasa
    return render(request,"passwdrcv.html",{'form':form, 'confirmacion':confirmacion})
#----------------------------------------------------------------------------------------------------------------------

#Restablecer Contraseña
def changepassword(request):
    form=RestablecerPassForm(request.POST or None)
    #Tengo que definir la variable msgbox antes con algun relleno o algo por que si no me da error, ya lo dije arriba :)
    msgbox=""
    #Pues aqui pide que intente recuperar el usuario
    try:
        username=request.GET["user"]
    except Exception as cosa:
        #Excepto cuando el nombre de usuario esta vacio o no coincide
        username= None
        #Si el nombre de usuario coincide bien pues continua a todo el chiche para restablecer la contraseña
    if username is not None:
        if form.is_valid():
            data=form.cleaned_data
            #Si la contraseña de la variable nuevapass coinvcide con nuevapasscheck entonces actualiza la contraseña del usuario por passwd que es nuevapasscheck
            if data.get("nuevapass") == data.get("nuevapasscheck"):
                passwd=make_password(data.get("nuevapasscheck"))
                User.objects.filter(username=username).update(password=passwd)
                msgbox="Contraseña cambiada exitosamente"
                #Te recomiendo anotarla en un papel para la proxima vez
            else:
                #Si no, te dice que no coincide y se arma la 3°a guerra termonueclear en tu PC
                msgbox="Las contraseñas deben coincidir, intentelo de nuevo"
                #Y como de costumbre, si todo sale  bkn te devuelve a la pagina y con el mesajito que te hace sentir satisfactorio en esta vida
        return render(request,"changepassword.html",{'form':form, 'username':username, 'msgbox':msgbox})
    else:
        return redirect('/login/')