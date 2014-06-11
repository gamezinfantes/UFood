from .models import Opinion
from django.forms import ModelForm


class OpinionForm(ModelForm):
    class Meta:
        model = Opinion
        fields = ['valoracion', 'puntuacion']
    

