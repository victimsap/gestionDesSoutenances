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
    sujet = models.OneToOneField(Sujet, on_delete=models.CASCADE)
    date = models.DateTimeField()
    salle = models.CharField(max_length=100)
    jury = models.CharField(max_length=255)

    def __str__(self):
        return f"Soutenance de {self.sujet.etudiant.nom}"

    def update_final_grade(self):
        from evaluations.models import Evaluation
        evaluations = self.evaluations.all()
        if evaluations.exists():
            self.final_grade = sum(e.note for e in evaluations) / evaluations.count()
            self.save()
