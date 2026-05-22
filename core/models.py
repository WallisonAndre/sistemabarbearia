from django.db import models


class ConfiguracaoBarbearia(models.Model):
    """Configurações gerais da barbearia — editável pelo dono."""
    nome = models.CharField(max_length=100, default='Minha Barbearia')
    slogan = models.CharField(max_length=200, blank=True)
    descricao = models.TextField(blank=True)
    foto_hero = models.ImageField(upload_to='barbearia/', blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_numero = models.CharField(max_length=20, blank=True, help_text='Ex: 5584999999999')
    endereco = models.CharField(max_length=255, blank=True)
    horario_funcionamento = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Configuração da Barbearia'
        verbose_name_plural = 'Configurações da Barbearia'

    def __str__(self):
        return self.nome


class Servico(models.Model):
    """Serviços oferecidos pela barbearia."""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_minutos = models.PositiveIntegerField(default=30)
    icone = models.CharField(
        max_length=50, blank=True,
        help_text='Classe do ícone (ex: bi-scissors)'
    )
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Barbeiro(models.Model):
    """Membros da equipe."""
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, default='Barbeiro')
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to='equipe/', blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True)
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    horarios_trabalho = models.TextField(blank=True, default='Seg a Sex: 09:00 - 19:00\nSáb: 09:00 - 17:00')
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Barbeiro'
        verbose_name_plural = 'Barbeiros'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class FotoGaleria(models.Model):
    """Galeria de fotos dos cortes."""
    barbeiro = models.ForeignKey(
        Barbeiro, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='fotos'
    )
    foto = models.ImageField(upload_to='galeria/')
    titulo = models.CharField(max_length=100, blank=True)
    descricao = models.CharField(max_length=255, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    destaque = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Foto da Galeria'
        verbose_name_plural = 'Fotos da Galeria'
        ordering = ['-destaque', '-data_upload']

    def __str__(self):
        return self.titulo or f'Foto {self.pk}'


class Produto(models.Model):
    """Produtos vendidos na barbearia."""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Venda(models.Model):
    """Venda de produtos."""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} em {self.data_venda.strftime("%d/%m/%Y")}'


class Agendamento(models.Model):
    """Agendamentos de serviços."""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente_nome = models.CharField(max_length=100)
    cliente_telefone = models.CharField(max_length=20)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_cobrado = models.DecimalField(max_digits=8, decimal_places=2)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data', '-hora_inicio']

    def __str__(self):
        return f'{self.cliente_nome} - {self.servico.nome} com {self.barbeiro.nome} ({self.data})'

