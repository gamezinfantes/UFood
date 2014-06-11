from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from .models import Cliente


class UserCreationFormExtend(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

ClienteFormset = inlineformset_factory(User, Cliente, 
        fields=('direccion','codigo_postal', 'telefono'), can_delete=False)