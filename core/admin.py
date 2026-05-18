from django.contrib import admin
from .models import ConfiguracaoBarbearia, Servico, Barbeiro, FotoGaleria


@admin.register(ConfiguracaoBarbearia)
class ConfiguracaoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidade', {'fields': ('nome', 'slogan', 'descricao', 'foto_hero')}),
        ('Contato & Redes', {'fields': ('instagram_url', 'whatsapp_numero')}),
        ('Informações', {'fields': ('endereco', 'horario_funcionamento')}),
    )


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao_minutos', 'ativo', 'ordem')
    list_editable = ('ativo', 'ordem', 'preco')
    list_filter = ('ativo',)
    search_fields = ('nome',)


@admin.register(Barbeiro)
class BarbeiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ativo', 'ordem')
    list_editable = ('ativo', 'ordem')
    search_fields = ('nome',)


@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'barbeiro', 'destaque', 'data_upload')
    list_editable = ('destaque',)
    list_filter = ('barbeiro', 'destaque')
    search_fields = ('titulo',)
