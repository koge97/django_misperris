from . import views
from django.conf.urls import url

urlpatterns=[
    url(r'^usuarios/$',views.gestionUsuario,name="gestionUsuario"),
    url(r'^login/$',views.ingresar,name="login"),
    url(r'^$',views.index,name="inicio"),
    url(r'^salir/$',views.salir,name="salir"),
]