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
    encadreur = models.ForeignKey(Encadreur, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.titre


class Soutenance(models.Model):
    sujet = models.OneToOneField(Sujet, on_delete=models.CASCADE, related_name='soutenance')

    # Corrige le problème "date_soutenance" → on garde ton champ "date"
    date = models.DateTimeField()

    salle = models.CharField(max_length=100)
    jury = models.CharField(max_length=255)
    final_grade = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', 'En attente'),
            ('programmee', 'Programmée'),
            ('realisee', 'Réalisée'),
            ('validee', 'Validée'),
        ],
        default='en_attente'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_final_grade(self):
        evaluations = self.evaluations.all()

        if evaluations.exists():
            avg = sum([e.note for e in evaluations]) / evaluations.count()
            self.final_grade = round(avg, 2)
            self.save(update_fields=['final_grade'])

        return self.final_grade

    def __str__(self):
        return f"Soutenance de {self.sujet.titre}"
