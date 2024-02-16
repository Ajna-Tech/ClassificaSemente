from django.forms import ModelForm
from .models import Sementes

class SementeForm(ModelForm):
    class Meta:
        model = Sementes
        fields = [
            'Defeito',
            'TipoDefeito',
            'IntensidadeDefeito',
            # 'Imagem',
            'Classificado'
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