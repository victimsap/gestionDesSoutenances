from django.db.models.signals import post_save
from django.dispatch import receiver

from rapports.models import Rapport
from soutenances.models import Soutenance
from evaluations.models import Evaluation
from notifications.models import Notification


# 1️⃣ Lorsqu’un rapport est déposé → notifier l'encadreur
@receiver(post_save, sender=Rapport)
def notify_encadreur_when_rapport_uploaded(sender, instance:Soutenance, created, **kwargs):
    if created:
        encadreur = instance.sujet.encadreur
        message = f"Un nouveau rapport pour le sujet '{instance.sujet.titre}' a été déposé."

        Notification.objects.create(
            user=encadreur,
            message=message,
            type="RAPPORT"
        )


# 2️⃣ Lorsqu’une soutenance est programmée → notifier l’étudiant
@receiver(post_save, sender=Soutenance)
def notify_student_when_soutenance_scheduled(sender, instance:Soutenance, created, **kwargs):
    if created:
        etudiant = instance.sujet.etudiant
        message = f"Votre soutenance a été programmée pour le {instance.date}."

        Notification.objects.create(
            user=etudiant,
            message=message,
            type="SOUTENANCE"
        )


# 3️⃣ Lorsqu’une évaluation est enregistrée → notifier l’étudiant
@receiver(post_save, sender=Evaluation)
def notify_student_when_evaluation_added(sender, instance:Evaluation, created, **kwargs):
    if created:
        etudiant = instance.soutenance.sujet.etudiant
        message = f"Une nouvelle note a été enregistrée pour votre soutenance."

        Notification.objects.create(
            user=etudiant,
            message=message,
            type="EVALUATION"
        )
