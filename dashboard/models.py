from django.db import models

# Create your models here.
from django.db import models

class Etudiant(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    matricule = models.CharField(max_length=100, unique=True)
    filiere = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Encadreur(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    specialite = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Sujet(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    encadreur = models.ForeignKey(Encadreur, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.titre


class Soutenance(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('programmee', 'Programmée'),
        ('realisee', 'Réalisée'),
        ('validee', 'Validée'),
    ]
    
    sujet = models.OneToOneField(Sujet, on_delete=models.CASCADE, related_name='soutenance')
    defense_date = models.DateField()
    defense_time = models.TimeField()
    room = models.CharField(max_length=100, verbose_name="Salle")
    jury = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='en_attente'
    )
    final_grade = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Note finale"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-defense_date']
    
    def __str__(self):
        return f"Soutenance de {self.sujet.etudiant.nom}"
    


