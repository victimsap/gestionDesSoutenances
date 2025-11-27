from django.contrib import admin
from .models import Etudiant, Encadreur, Sujet, Soutenance

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['id','nom','prenom','matricule','filiere']
    search_fields = ['nom','prenom','matricule']

@admin.register(Encadreur)
class EncadreurAdmin(admin.ModelAdmin):
    list_display = ['id','nom','prenom','specialite']
    search_fields = ['nom','prenom','specialite']

@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ['id','titre','etudiant','encadreur']
    search_fields = ['titre','etudiant__nom','encadreur__nom']

@admin.register(Soutenance)
class SoutenanceAdmin(admin.ModelAdmin):
    list_display = ['id','sujet','date','salle','jury']
    search_fields = ['sujet__titre','salle','jury']
    list_filter = ['date']
