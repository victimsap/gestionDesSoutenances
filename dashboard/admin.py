from django.contrib import admin
from .models import Etudiant, Encadreur, Sujet, Soutenance


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenom', 'filiere']
    search_fields = ['nom', 'prenom', 'matricule']
    list_filter = ['filiere']


@admin.register(Encadreur)
class EncadreurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'specialite']
    search_fields = ['nom', 'prenom', 'specialite']
    list_filter = ['specialite']


@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ['titre', 'etudiant', 'encadreur']
    search_fields = ['titre', 'description']
    list_filter = ['etudiant', 'encadreur']
    autocomplete_fields = ['etudiant', 'encadreur']


@admin.register(Soutenance)
class SoutenanceAdmin(admin.ModelAdmin):
    list_display = [
        'get_etudiant', 
        'get_sujet', 
        'defense_date',      # ← Changé de 'date' à 'defense_date'
        'defense_time',      # ← Ajouté
        'room',              # ← Changé de 'salle' à 'room'
        'status',            # ← Ajouté
        'final_grade'        # ← Ajouté
    ]
    list_filter = [
        'status',            # ← Changé de 'date' à 'status'
        'defense_date',      # ← Ajouté pour filtrer par date
    ]
    search_fields = [
        'sujet__titre', 
        'sujet__etudiant__nom', 
        'sujet__etudiant__prenom',
        'jury'
    ]
    date_hierarchy = 'defense_date'  # ← Changé de 'date' à 'defense_date'
    ordering = ['-defense_date', '-defense_time']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('sujet', 'status')
        }),
        ('Détails de la soutenance', {
            'fields': ('defense_date', 'defense_time', 'room', 'jury')
        }),
        ('Évaluation', {
            'fields': ('final_grade',),
            'classes': ('collapse',)
        }),
    )
    
    def get_etudiant(self, obj):
        """Affiche le nom de l'étudiant"""
        return f"{obj.sujet.etudiant.prenom} {obj.sujet.etudiant.nom}"
    get_etudiant.short_description = 'Étudiant'
    get_etudiant.admin_order_field = 'sujet__etudiant__nom'
    
    def get_sujet(self, obj):
        """Affiche le titre du sujet"""
        return obj.sujet.titre
    get_sujet.short_description = 'Sujet'
    get_sujet.admin_order_field = 'sujet__titre'