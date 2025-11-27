from django.db import models
from django.conf import settings  # ← Important pour utiliser le Custom User

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← Utilise le modèle utilisateur défini dans settings
        related_name="notifications",
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif → {self.user.username}"
