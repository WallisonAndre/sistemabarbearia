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
        'dias_semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
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


def agendar(request):
    config = get_config()
    servicos = Servico.objects.filter(ativo=True)
    barbeiros = Barbeiro.objects.filter(ativo=True)
    
    context = {
        'config': config,
        'servicos': servicos,
        'barbeiros': barbeiros,
    }
    return render(request, 'core/agendar.html', context)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def api_agendar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            servico = Servico.objects.get(id=data['servico_id'])
            barbeiro = Barbeiro.objects.get(id=data['barbeiro_id'])
            
            data_agendamento = datetime.datetime.strptime(data['data'], '%Y-%m-%d').date()
            hora_inicio = datetime.datetime.strptime(data['hora'], '%H:%M').time()
            
            # Calcular hora fim baseada na duração do serviço
            duracao = datetime.timedelta(minutes=servico.duracao_minutos)
            hora_inicio_dt = datetime.datetime.combine(data_agendamento, hora_inicio)
            hora_fim_dt = hora_inicio_dt + duracao
            hora_fim = hora_fim_dt.time()
            
            from .models import Agendamento
            agendamento = Agendamento.objects.create(
                cliente_nome=data['nome'],
                cliente_telefone=data['telefone'],
                servico=servico,
                barbeiro=barbeiro,
                data=data_agendamento,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                status='pendente',
                valor_cobrado=servico.preco
            )
            
            return JsonResponse({'status': 'success', 'id': agendamento.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

@staff_member_required
def dashboard(request):
    config = get_config()
    hoje = datetime.date.today()
    
    from .models import Agendamento, Venda, Produto
    
    # Resumo Rápido
    agendamentos_hoje = Agendamento.objects.filter(data=hoje)
    total_cortes = agendamentos_hoje.count()
    
    # Faturamento de agendamentos concluidos hoje
    faturamento_cortes = agendamentos_hoje.filter(status='concluido').aggregate(Sum('valor_cobrado'))['valor_cobrado__sum'] or 0
    
    # Produtos vendidos hoje
    vendas_hoje = Venda.objects.filter(data_venda__date=hoje)
    faturamento_produtos = vendas_hoje.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    produtos_vendidos = vendas_hoje.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    
    faturamento_total = faturamento_cortes + faturamento_produtos
    
    # Agenda da equipe (Timeline)
    barbeiros = Barbeiro.objects.filter(ativo=True)
    agenda_equipe = []
    
    for barbeiro in barbeiros:
        horarios = agendamentos_hoje.filter(barbeiro=barbeiro).order_by('hora_inicio')
        agenda_equipe.append({
            'barbeiro': barbeiro,
            'agendamentos': horarios
        })
        
    context = {
        'config': config,
        'total_cortes': total_cortes,
        'faturamento_total': faturamento_total,
        'produtos_vendidos': produtos_vendidos,
        'agenda_equipe': agenda_equipe,
        'hoje': hoje,
    }
    return render(request, 'core/dashboard.html', context)

