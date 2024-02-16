from base64 import b64encode
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Sementes
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Sementes
from .forms import SementeForm
from django.contrib.auth.decorators import login_required

def classificaSementeInicial(request):
    sementesList = Sementes.objects.all().order_by('Id')
    paginator = Paginator(sementesList, 15)
    page = request.GET.get('page')
    
    sementes = paginator.get_page(page)
    
    context = {'sementes': sementes}
    return render(request, 'sementes/classificaSementeInicial.html', context)

# @login_required
def classificacao(request, id):
    semente = get_object_or_404(Sementes, Id = id)
    updateSemente = SementeForm(instance=semente)
    if request.method == 'POST':
        updateSemente = SementeForm(request.POST or None)
        if updateSemente.is_valid():
            updateSemente.save()
            return redirect('/sementes/classificaSementeInicial')
        else:
            context = {'updateSemente' : updateSemente, 'semente' : semente}
            return render(request, 'sementes/classificacaoSemente.html', context)
    else:
        context = {'updateSemente' : updateSemente, 'semente' : semente}
        return render(request, 'sementes/classificacaoSemente.html', context)