from django.http import JsonResponse
from soutenances.models import Soutenance, Sujet
from users.models import User
from rapports.models import Rapport
from evaluations.models import Evaluation
from django.db.models import Avg, Count


def stats(request):
    """
    Dashboard simple avec les statistiques principales.
    """

    # Comptage des utilisateurs par rôle
    users_by_role = User.objects.values("role").annotate(total=Count("id"))

    data = {
        "total_users": User.objects.count(),
        "users_by_role": list(users_by_role),

        "total_soutenances": Soutenance.objects.count(),
        "total_sujets": Sujet.objects.count(),
        "total_rapports": Rapport.objects.count(),
        "total_evaluations": Evaluation.objects.count(),

        # moyenne des notes
        "moyenne_notes": Evaluation.objects.aggregate(avg=Avg("note"))["avg"] or 0,

        # statut des soutenances
        "soutenances_par_statut": list(
            Soutenance.objects.values("status").annotate(total=Count("id"))
        ),
    }

    return JsonResponse(data, safe=False)
