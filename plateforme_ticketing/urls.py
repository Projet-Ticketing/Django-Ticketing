"""
URL configuration for plateforme_ticketing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path('', views.connexion, name='connexion'),
    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('creer-ticket/', views.creer_ticket, name='creer_ticket'),
    path('espace/', views.espace_utilisateur, name='espace_utilisateur'),
    path('ticket/<int:ticket_id>/', views.detail_ticket, name='detail_ticket'),
    path('espace-technicien/', views.espace_technicien, name='espace_technicien'),
    path('attribuer-ticket/<int:ticket_id>/', views.attribuer_ticket, name='attribuer_ticket'),
    path('cloturer-ticket/<int:ticket_id>/', views.cloturer_ticket, name='cloturer_ticket'),
    path('logout/', views.deconnexion, name='logout'),
    path('statistiques/', views.statistiques, name='statistiques'),
]
