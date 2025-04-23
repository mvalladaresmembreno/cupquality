from django import forms
from .models import Colaborador
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['firma']
        