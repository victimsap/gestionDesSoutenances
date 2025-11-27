from django.db.models.signals import post_save
from django.dispatch import receiver

from rapports.models import Rapport
from soutenances.models import Soutenance
from evaluations.models import Evaluation
from notifications.models import Notification


# 1️⃣ Lorsqu’un rapport est déposé → notifier encadreur
@receiver(post_save, sender=Rapport)
def notify_encadreur_when_rapport_uploaded(sender, instance, created, **kwargs):
    if created:
        encadreur = instance.sujet.encadreur  
        message = f"Un nouveau rapport pour le sujet '{instance.sujet.title}' a été déposé."
        Notification.objects.create(user=encadreur, message=message)


# 2️⃣ Lorsqu’une date de soutenance est fixée → notifier étudiant
@receiver(post_save, sender=Soutenance)
def notify_student_when_soutenance_scheduled(sender, instance, created, **kwargs):
    if created:
        etudiant = instance.etudiant  
        message = f"Votre soutenance a été programmée pour le {instance.date_soutenance}."
        Notification.objects.create(user=etudiant, message=message)


# 3️⃣ Lorsqu’une évaluation est enregistrée → notifier étudiant
@receiver(post_save, sender=Evaluation)
def notify_student_when_evaluation_added(sender, instance, created, **kwargs):
    if created:
        etudiant = instance.soutenance.etudiant
        message = f"Une nouvelle note a été ajoutée pour votre soutenance."
        Notification.objects.create(user=etudiant, message=message)
