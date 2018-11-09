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
    url(r'^deleteuser/(?P<id>\d+)/$',views.deleteuser, name="deleteuser"),
    url(r'^regusr/$',views.regusr,name="regusr"),
    url(r'^regpet/$',views.regpet,name="regpet"),
    url(r'^mngrpet/$',views.mngrpets, name="mngrpet"),
    url(r'^deletepet/(?P<id>\d+)/$',views.deletepet, name="deletepet"),
    url(r'^adoptpet/$',views.adoptpets, name="adoptpet"),
    url(r'^editpet/(?P<id>\d+)/$',views.petupdate, name="editpet"),
]