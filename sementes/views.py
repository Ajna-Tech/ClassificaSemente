from base64 import b64encode
from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Sementes
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Sementes
from .forms import BulkSementeForm, SementeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max

@login_required
def classificaSementeInicial(request):
    sementesList = Sementes.objects.all().order_by('Id')
    paginator = Paginator(sementesList, 15)
    page = request.GET.get('page')
    
    sementes = paginator.get_page(page)
    
    context = {'sementes': sementes}
    return render(request, 'sementes/classificaSementeInicial.html', context)

@login_required
def classifica(request):
    # Determina o ID máximo
    id_maximo = Sementes.objects.aggregate(Max('Id'))['Id__max']

    # Define os intervalos de IDs para cada lote de 1000
    intervalos = [(i, min(i + 999, id_maximo)) for i in range(1, id_maximo + 1, 1000)]

    # Itera sobre os intervalos para encontrar a primeira semente não classificada em cada lote
    for inicio, fim in intervalos:
        proxima_semente = Sementes.objects.filter(Id__range=(inicio, fim), Classificado=False).first()
        if proxima_semente:
            return redirect('classificaSemente', id=proxima_semente.Id)

    # Se todas as sementes estiverem classificadas, redireciona para uma página padrão
    return redirect('classificaSementeInicial')


@login_required
def classificacao(request, id):
    semente_atual = get_object_or_404(Sementes, Id=id)
    proxima_semente = Sementes.objects.filter(Id__gt=id, Classificado=False).order_by('Id').first()

    if request.method == 'POST':
        updateSemente = SementeForm(request.POST, instance=semente_atual)
        if 'classificar' in request.POST:  # Verifica se o botão 'Classificar' foi clicado
            if updateSemente.is_valid():
                semente_atual = updateSemente.save(commit=False)
                semente_atual.Classificado = True  # Define 'Classificado' como True
                semente_atual.save()
                
                # Redireciona para a próxima semente, se houver
                if proxima_semente:
                    return redirect('classificaSemente', id=proxima_semente.Id)
                else:
                    return redirect('classificaSementeInicial')
        else:
            if updateSemente.is_valid():
                updateSemente.save()
                return redirect('classificaSementeInicial')

    context = {'updateSemente': SementeForm(instance=semente_atual), 'semente': semente_atual}
    return render(request, 'sementes/classificacaoSemente.html', context)

@login_required
def criar_sementes_em_massa(request):
    if request.method == 'POST':
        form = BulkSementeForm(request.POST, request.FILES)
        if form.is_valid():
            for imagem in request.FILES.getlist('Imagem'):
                # Criar uma instância do formulário com os dados do arquivo atual
                form_instancia = BulkSementeForm({'Imagem': imagem})
                if form_instancia.is_valid():
                    # Salvar a instância do formulário sem fazer commit (commit=False)
                    semente = form_instancia.save(commit=False)
                    # Atribuir os valores necessários aos outros campos do modelo
                    semente.Imagem = imagem
                    semente.Defeito = False
                    semente.TipoDefeito = None
                    semente.IntensidadeDefeito = None
                    semente.Classificado = False
                    # Salvar a instância final no banco de dados
                    semente.save()
            return redirect('classificaSementeInicial')
    else:
        form = BulkSementeForm()
    return render(request, 'sementes/criaSementes.html', {'form': form})