from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from reservas.models import Reserva

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'rol')

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'rol')

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

