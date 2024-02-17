from django import forms
from django.forms import ClearableFileInput, FileField, ModelForm, ValidationError
from .models import Sementes

class SementeForm(ModelForm):
    class Meta:
        model = Sementes
        fields = [
            'Defeito',
            'TipoDefeito',
            'IntensidadeDefeito'
        ]
        
        labels = {
            'Defeito': ('Defeito'),
            'TipoDefeito': ('Tipo de Defeito'),
            'IntensidadeDefeito': ('Intensidade do Defeito'),
            'Classificado': ('Classificado'),
        }
    def __init__(self, *args, **kwargs):
        super(SementeForm, self).__init__(*args, **kwargs)
        
        if self.fields["Defeito"] == True:
            self.fields["TipoDefeito"].required = True
            self.fields["IntensidadeDefeito"].required = True

class MultiFileField(FileField):
    def to_python(self, data):
        if not data:
            return []
        elif not isinstance(data, list):
            raise ValidationError('FileField expects a list of files.')
        return data

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class BulkSementeForm(ModelForm):
    Imagem = MultipleFileField(label='Imagens', required=False)
    class Meta:
        model = Sementes
        fields = ('Imagem',)