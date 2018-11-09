#Importa los formularios AgregarUsuario, LoginForm, RestablecerPassForm, RestablecerPassMail
from .forms import AgregarUsuario, LoginForm, RestablecerPassForm, RestablecerPassMail, RegUsr, AgregarMascota
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
from .models import Usuario, Mascota
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

# Parto agradeciendo y dedicando unas palabras sensuales, aguante StackOverflow y la documentacion de Django por sacarme las dudas :)

#----------------------------------------------------------------------------------------------------------------------


#Index
def index(request):
    #Deje comentadas estas lineas de abajo por que estoy probando como meter las imagenes de la DB al BxSlider
    #pantalla=get_template("index.html")
    #contexto={'titulo':"Index",}
    #Creo que ya se sabe para que es esto, si no, pues mete todas las mascotas en la variable lista etc etc
    lista = Mascota.objects.all()
    #Ya mostremos el index pls
    return render(request, 'index.html', {'lista':lista})
    #return HttpResponse(pantalla.render(contexto,request))

#----------------------------------------------------------------------------------------------------------------------

#Gestion de Usuarios desde Admin
@login_required(login_url="login")
@staff_member_required
def gestionUsuario(request):
    #Aqui meteremos los usuarios
    usuarios=User.objects.all()
    #Y aqui meteremos el resto de datos de los usuarios por que django solo deja meter 3 a 4 parametros pal user idk why (no pregunten por que se llama 'cosita', es lo que se me ocurrio)
    cositas=Usuario.objects.all()
    #Hora del formulario!
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
        return redirect('clientes')
    form=AgregarUsuario()
    return render(request,"GestionarUsuario.html",{'form':form,'usuarios':usuarios,'cositas':cositas})
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
        #Si el usuarios es distinto a none pos nos logeamos y nos vamos para la gestion
        if user is not None:
            login(request, user)
            #Cachilupi cierto?
            return redirect('inicio')
    return render(request,"login.html",{'form':form})

#----------------------------------------------------------------------------------------------------------------------

#Salir
@login_required(login_url="login")
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
    #Si el formulario es valido hace el get del username y manda un sensual correo a la direccion que tenga guardada esta cosa a travez del send_mail
    #Estuve hasta las 4AM tratando de hacer que funcionara y despues me di cuenta que tenia mal escrito el snmp de Google pal Gmail :D (De hecho creo que lo escribi mal de nuevo xd)
    if form.is_valid():
        data=form.cleaned_data
        usuario=User.objects.get(username=data.get("username"))
        send_mail(
                'Recuperar Password',
                #Juguemos Fortnite? Okno.
                'Me gusta el Fortnite lo juego todo el dia esto no es Minecraft me encanta es muy bueno',
                #Aguanten las Guias de Django y StackOverflow, no se que hace esto pero funciona.
                'from@example.com',
                #Esto pide el mail con el que el usuario se registro
                [usuario.email],
                #Y aqui va el mensaje, que maravilla verdad?
                html_message='Pinchando el siguiente <a href="http://localhost:8000/changepassword?user='+usuario.username+'">enlace</a> podras restablecer tu contraseña',
            )
        return redirect('login')
        #Si todo sale ok te devuelve al formulario pero con el mensaje de arriba confirmado que se envio el mail, si no, pues anda a rezarle a la virgencita que algo pasa
    return render(request,"passwdrcv.html",{'form':form})
#----------------------------------------------------------------------------------------------------------------------

#Restablecer Contraseña
def changepassword(request):
    form=RestablecerPassForm(request.POST or None)
    username=request.GET["user"]
    if username is not None:
        if form.is_valid():
            data=form.cleaned_data
            #Si la contraseña de la variable nuevapass coinvcide con nuevapasscheck entonces actualiza la contraseña del usuario por passwd que es nuevapasscheck
            if data.get("nuevapass") == data.get("nuevapasscheck"):
                passwd=make_password(data.get("nuevapasscheck"))
                User.objects.filter(username=username).update(password=passwd)
                #Te recomiendo anotarla en un papel para la proxima vez
                #Y como de costumbre, si todo sale  bkn te devuelve a la pagina del login
                return redirect('/login/')
        return render(request,"changepassword.html",{'form':form, 'username':username})
    else:
        return redirect('/login/')

#----------------------------------------------------------------------------------------------------------------------
#Esta parte nos va a listar los adoptantes, me dio paja cambiarle el nombre de clientes por que era una prueba inicial y pos se quedo asi
@login_required(login_url="login")
@staff_member_required
def clientes(request):  
    #Pescamos todos los usuarios y los metemos a la lista y era
    lista = Usuario.objects.all()
    #Rendereamos el mantenedor de clientes
    return render(request, 'clientes.html', {'lista':lista})

#----------------------------------------------------------------------------------------------------------------------

#Aqui eliminaremos clientes, gracias jorge por la ayuda xd
#Tenemos que pedir el ID en el request
@login_required(login_url="login")
@staff_member_required
def deleteuser(request,id):
    #Luego en el get pedimos el id igual y se lo pasamos al placeholder
    placeholder=Usuario.objects.get(id=id)
    if request.method=='POST':
        #Chao no vimo bendisiune bai bai
        placeholder.delete()
        #Y nos devolvemos al mantenedor de clientes
        return redirect('clientes')
    return render(request,'deleteuser.html',{'placeholder':placeholder})

#----------------------------------------------------------------------------------------------------------------------

#Registro comun y silvestre, un simple copy y paste de lo que hay mas arriba pero con unos detallitos mas sensualones

def regusr(request):
    usuarios=User.objects.all()
    cositas=Usuario.objects.all()
    form=RegUsr(request.POST)
    if form.is_valid():
        data=form.cleaned_data
        #Aqui va a crear el usuario con los tres parametros principales
        u=User.objects.create_user(data.get("username"),data.get("correo"),data.get("password"))
        #define la variable var_rol como lo que tenga el rol
        var_rol="Normal"
        #Si el rol es normal pues la cuenta que este creando no es staff/admin/superusuario o como le digas
        if var_rol == "Normal":
            u.is_staff=False
            #Si es cualquier otra cosa (Que solo puede ser admin asdasjdasd) sera staff
        else:
            u.is_staff=True
            #Aqui guarda el usuario
        u.save()
        #Aqui obtiene el resto de datos para meterlos en la tabla usuario
        regDB=Usuario(nombre=data.get("nombre"),apellido=data.get("apellido"),fecha=data.get("fecha"),region=data.get("region"),ciudad=data.get("ciudad"),vivienda=data.get("vivienda"),user=u)
        #Y aqui los guarda c:
        regDB.save()
        return redirect('login')
    form=RegUsr()
    return render(request,"regusr.html",{'form':form,'usuarios':usuarios,'cositas':cositas})
#NOTA: Despues de lesear como 2 horas por que no me tomaba la tabla Usuario, solo habia que hacer un > python manage.py migrate --run-syncdb

#----------------------------------------------------------------------------------------------------------------------

#Registra una mascota
@login_required(login_url="login")
@staff_member_required
def regpet(request):
    #Pescamos todos los objetos de la tabla mascota y los metemos en pets
    pets=Mascota.objects.all()
    form=AgregarMascota(request.POST, request.FILES)
    if form.is_valid():
        data=form.cleaned_data
        #Aqui viene lo lindo, metemos todo en el regdb y guardamos
        regDB=Mascota(nombre=data.get("nombre"),raza=data.get("raza"),descripcion=data.get("descripcion"),estado=data.get("estado"),pic=request.FILES['pic'])
        #Wingardium leviosa!!!!!!!!!!!!11
        regDB.save()
        return redirect('mngrpet')
    form=AgregarMascota()
    #En la practica es lo mismo que ingresar un usuario nuevo solo que se va a otra tabla xD
    return render(request,"regpet.html",{'form':form,'pets':pets})

#----------------------------------------------------------------------------------------------------------------------
#Enlista las mascotas, lo mismo de arriba
# def mngrpets(request):  
#     #Bla bla pescamos de mascota metemos en lista y chao
#     lista = Mascota.objects.all()
#     #y rendereamos el manager
#     return render(request, 'mngrpet.html', {'lista':lista})
#Dejo todo esto comentado por que quiero probar el paginator :)
#----------------------------------------------------------------------------------------------------------------------

#LO MISMO DE ARRIBA PA ELIMINAR GENTE PERO AHORA ELIMINAMOS MASCOTAS >:C    ̶(E̶N̶ ̶V̶E̶Z̶ ̶D̶E̶ ̶E̶L̶I̶M̶I̶N̶A̶R̶ ̶S̶E̶R̶E̶S̶ ̶H̶U̶M̶A̶N̶O̶S̶)
@login_required(login_url="login")
@staff_member_required
def deletepet(request,id):
    placeholder=Mascota.objects.get(id=id)
    if request.method=='POST':
        #No voy a explicar esto de nuevo
        placeholder.delete()
        return redirect('mngrpet')
    return render(request,'deletepet.html',{'placeholder':placeholder})

#----------------------------------------------------------------------------------------------------------------------

#Otra vez lo mismo, pero aqui enlistamos las mascotas para el lado del adoptante sin privilegios de staff... ni un brillo
# def adoptpets(request):  
#     lista = Mascota.objects.all()
#     return render(request, 'adoptpet.html', {'lista':lista})

#PAGINATOR PARA ADOPTAR PETS
@login_required(login_url="login")
def adoptpets(request):  
    form=AgregarMascota(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        Mascota.objects.create(nombre=data.get("nombre"),raza=data.get("raza"),descripcion=data.get("descripcion"),estado=data.get("estado"),pic=request.FILES['pic'])
    form=AgregarMascota()
    mascotas=Mascota.objects.all()
    paginator=Paginator(mascotas,3)

    try:
        pag=int(request.GET.get("page",1))
    except ValueError:
        pag=1

    try:
        mascotas=paginator.page(pag)
    except (InvalidPage, EmptyPage):
        mascotas=paginator.page(paginator.num_pages)
    
    contexto={"mascotas":mascotas,"form":form}
    return render(request,'adoptpet.html',contexto)
#----------------------------------------------------------------------------------------------------------------------
#Actualizar una mascotas
#Tomamos los datos con el POST y los metemos de nuevo c:
@login_required(login_url="login")
@staff_member_required
def petupdate(request,id):
    regDB=Mascota.objects.get(id=id)
    if request.method=="POST":
        form=AgregarMascota(request.POST, request.FILES)
        if form.is_valid():
            data=form.cleaned_data
            regDB.nombre=data.get("nombre")
            regDB.raza=data.get("raza")
            regDB.descripcion=data.get("descripcion")
            regDB.estado=data.get("estado")
            regDB.pic=request.FILES['pic']
            regDB.save()
            return redirect("mngrpet")
    else:
        data={
            "nombre":regDB.nombre,
            "raza":regDB.raza,
            "descripcion":regDB.descripcion,
            "estado":regDB.estado
        }
        form=AgregarMascota(data)
    return render(request, "editpet.html", {"form":form})

#----------------------------------------------------------------------------------------------------------------------
#Otro paginator mas
@login_required(login_url="login")
@staff_member_required
def mngrpets(request):  
    form=AgregarMascota(request.POST or None)
    if form.is_valid():
        data=form.cleaned_data
        Mascota.objects.create(nombre=data.get("nombre"),raza=data.get("raza"),descripcion=data.get("descripcion"),estado=data.get("estado"),pic=request.FILES['pic'])
    form=AgregarMascota()
    mascotas=Mascota.objects.all()
    paginator=Paginator(mascotas,3)

    try:
        pag=int(request.GET.get("page",1))
    except ValueError:
        pag=1

    try:
        mascotas=paginator.page(pag)
    except (InvalidPage, EmptyPage):
        mascotas=paginator.page(paginator.num_pages)
    
    contexto={"mascotas":mascotas,"form":form}
    return render(request,'mngrpet.html',contexto)
#----------------------------------------------------------------------------------------------------------------------

#Ya me dio flojera seguir comentando