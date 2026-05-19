from django.shortcuts import render
from .models import ConfiguracaoBarbearia, Servico, Barbeiro, FotoGaleria

def get_config():
    return ConfiguracaoBarbearia.objects.first()

def home(request):
    config = get_config()
    servicos = Servico.objects.filter(ativo=True)
    barbeiros = Barbeiro.objects.filter(ativo=True)

    context = {
        'config': config,
        'servicos': servicos,
        'barbeiros': barbeiros,
    }
    return render(request, 'core/home.html', context)


def sobre(request):
    config = get_config()
    context = {
        'config': config,
    }
    return render(request, 'core/sobre.html', context)


def galeria(request):
    config = get_config()
    fotos = FotoGaleria.objects.all()
    barbeiros = Barbeiro.objects.filter(ativo=True)

    barbeiro_id = request.GET.get('barbeiro')
    if barbeiro_id:
        fotos = fotos.filter(barbeiro_id=barbeiro_id)

    context = {
        'config': config,
        'fotos': fotos,
        'barbeiros': barbeiros,
        'barbeiro_selecionado': barbeiro_id,
    }
    return render(request, 'core/galeria.html', context)
