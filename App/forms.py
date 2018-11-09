from django import forms

#Agregar un Usuario desde una cuenta con privilegios
class AgregarUsuario(forms.Form):
    correo=forms.EmailField(widget=forms.EmailInput(),label="Correo")
    username=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")
    nombre=forms.CharField(widget=forms.TextInput(),label="Nombre")
    apellido=forms.CharField(widget=forms.TextInput(),label="Apellido")
    fecha=forms.DateField(widget=forms.SelectDateWidget(years=range(1973,2001)),label="Fecha de Nacimiento")
    region=forms.ChoiceField(choices=(('1', 'RM REGION METROPOLITANA',),),label="Región")
    ciudad=forms.ChoiceField(choices=(('1', 'Ñuñoa la lleva',),),label="Ciudad")
    vivienda=forms.ChoiceField(choices=(('Casa con Patio Grande', 'Casa con Patio Grande'),('Casa con Patio Pequeño', 'Casa con Patio Pequeño'),('Casa sin Patio', 'Casa sin Patio'),('Departamento', 'Departamento')),label="Vivienda")
    rol=forms.ChoiceField(choices=(('Normal', 'Normal'),('Admin','Admin'),),label="Rol del Usuario")

#Registro de Usuario comun y silvestre
class RegUsr(forms.Form):
    correo=forms.EmailField(widget=forms.EmailInput(),label="Correo")
    username=forms.CharField(widget=forms.TextInput(),label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput(),label="Contraseña")
    nombre=forms.CharField(widget=forms.TextInput(),label="Nombre")
    apellido=forms.CharField(widget=forms.TextInput(),label="Apellido")
    fecha=forms.DateField(widget=forms.SelectDateWidget(years=range(1973,2001)),label="Fecha de Nacimiento")
    region=forms.ChoiceField(choices=(('1', 'RM REGION METROPOLITANA',),),label="Región")
    ciudad=forms.ChoiceField(choices=(('1', 'Ñuñoa la lleva',),),label="Ciudad")
    vivienda=forms.ChoiceField(choices=(('Casa con Patio Grande', 'Casa con Patio Grande'),('Casa con Patio Pequeño', 'Casa con Patio Pequeño'),('Casa sin Patio', 'Casa sin Patio'),('Departamento', 'Departamento')),label="Vivienda")
#Login? xD
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
#Agrega las mascotas
class AgregarMascota(forms.Form):
    pic=forms.ImageField(label="Imagen")
    nombre=forms.CharField(widget=forms.TextInput(),label="Nombre")
    raza=forms.CharField(widget=forms.TextInput(),label="Raza")
    descripcion=forms.CharField(widget=forms.TextInput(),label="Descripcion")
    estado=forms.ChoiceField(choices=(('Rescatado', 'Rescatado'),('Disponible', 'Disponible'),('Adoptado', 'Adoptado')),label="Estado")
