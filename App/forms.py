from django import forms

#Agregar un Usuario normal
class AgregarUsuario(forms.Form):
    correo=forms.EmailField(widget=forms.EmailInput(),label="Correo")
    username=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")
    nombre=forms.CharField(widget=forms.TextInput(),label="Nombre")
    apellido=forms.CharField(widget=forms.TextInput(),label="Apellido")
    fecha=forms.DateField(widget=forms.SelectDateWidget(years=range(1973,2001)),label="Fecha de Nacimiento")
    region=forms.ChoiceField(choices=(('1', 'RM REGION METROPOLITANA',),),label="Región")
    ciudad=forms.ChoiceField(choices=(('1', 'Ñuñoa la lleva',),),label="Ciudad")
    vivienda=forms.ChoiceField(choices=(('1', 'Casa con Patio Grande'),('2', 'Casa con Patio Pequeño'),('3', 'Casa sin Patio'),('4', 'Departamento')),label="Vivienda")
    rol=forms.ChoiceField(choices=(('1', 'Normal'),('2','Admin'),),label="Rol del Usuario")

class LoginForm(forms.Form):
    usr=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    passwd=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")

#Restablecer Password
class RestablecerPassForm(forms.Form):
    nuevapass=forms.CharField(widget=forms.PasswordInput(),label="Escriba su nueva Password")
    nuevapasscheck=forms.CharField(widget=forms.PasswordInput(),label="Repita su nueva Password")

#Mail Restablece Contraseña
class RestablecerPassMail(forms.Form):
    username=forms.CharField(widget=forms.TextInput(),label="Usuario")

