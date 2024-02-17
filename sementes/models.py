from django.db import models

class ClasseDefeito(models.IntegerChoices):
    SemDefeito = 0
    Leve = 1
    Severo = 2
        
class TipoDefeito(models.TextChoices):
    NA = "NA"
    Ardido = "Ardido"
    Furado = "Furado"
    Quebrado = "Quebrado"
    PoppedKernel = "Popped Kernel"

class Sementes(models.Model):
    Id = models.IntegerField(primary_key=True)
    Defeito = models.BooleanField(default=False)
    TipoDefeito = models.CharField(max_length=20, choices=TipoDefeito.choices, default=None, blank=True, null=True)
    IntensidadeDefeito = models.IntegerField(choices=ClasseDefeito, default=None, blank=True, null=True)
    Imagem = models.ImageField(upload_to='sementes/imagens/')
    Classificado = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.Id)