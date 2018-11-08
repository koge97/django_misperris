from django.db import models
from django.contrib.auth.models import User
# Create your models here.



#Creditos a este compadre que se las sabe todas https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
#Cualquier cambio correr un >python manage.py migrate --run-syncdb
class Usuario(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=20)
    apellido=models.CharField(max_length=30)
    fecha=models.DateField()
    region=models.CharField(max_length=20)
    ciudad=models.CharField(max_length=20)
    vivienda=models.CharField(max_length=20)
    rol=models.CharField(max_length=10, default="Normal")