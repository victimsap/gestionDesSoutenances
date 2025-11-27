from django.db import models
from django.conf import settings
from soutenances.models import Sujet, Soutenance  # <-- importer Soutenance

User = settings.AUTH_USER_MODEL

def rapport_upload_path(instance, filename):
    return f"rapports/sujet_{instance.sujet.id}/{filename}"

class Rapport(models.Model):
    sujet = models.ForeignKey(
        Sujet,
        related_name='rapports',
        on_delete=models.CASCADE
    )

    # 🔥 AJOUT : relation avec Soutenance
    soutenance = models.OneToOneField(
        Soutenance,
        related_name='rapport',
        on_delete=models.CASCADE,
        null=True,        # Pour éviter les erreurs après migration
        blank=True
    )

    file = models.FileField(upload_to=rapport_upload_path)
    uploaded_by = models.ForeignKey(
        User,
        related_name='rapports_uploads',
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Rapport {self.sujet.title} ({self.uploaded_by})"
