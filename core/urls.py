from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('galeria/', views.galeria, name='galeria'),
    path('agendar/', views.agendar, name='agendar'),
    path('api/agendar/', views.api_agendar, name='api_agendar'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
