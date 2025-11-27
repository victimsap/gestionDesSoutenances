from django.db import models
from django.conf import settings
from soutenances.models import Soutenance

class Evaluation(models.Model):
    soutenance = models.ForeignKey(Soutenance, related_name="evaluations", on_delete=models.CASCADE)
    jury = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commentaire = models.TextField(null=False, blank=False, verbose_name="Commentaire du jury")
    note = models.FloatField(null=False, verbose_name="Note obtenue")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.soutenance.update_final_grade()

    def __str__(self):
        return f"Evaluation de {self.soutenance.sujet.etudiant.nom} par {self.jury.username}"
