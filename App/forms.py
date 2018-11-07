from django import forms
class AgregarUsuario(forms.Form):
    correo=forms.EmailField(widget=forms.EmailInput(),label="Correo")
    username=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")
    
#Restablecer Password
class RestablecerPassForm(forms.Form):
    nuevapass=forms.CharField(widget=forms.PasswordInput(),label="Escriba su nueva Password")
    nuevapasscheck=forms.CharField(widget=forms.PasswordInput(),label="Repita su nueva Password")