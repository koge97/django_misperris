from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^addusradmin/$',views.gestionUsuario,name="gestionUsuario"),
    url(r'^mngrusr/$',views.clientes, name="clientes"), 
    url(r'^login/$',views.ingresar,name="login"),
    url(r'^$',views.index,name="inicio"),
    url(r'^salir/$',views.salir,name="salir"),
    url(r'^passwdrcv/$',views.recovery,name="recovery"),
    url(r'^changepassword/$',views.changepassword,name="changepassword"),
]