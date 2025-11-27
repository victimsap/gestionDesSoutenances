from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Evaluation
from .serializers import EvaluationSerializer

# Vue classique pour la page d'accueil de l'app "evaluations"
def index(request):
    return HttpResponse("Bienvenue sur l'application Évaluations !")

# ViewSet DRF pour gérer l'API CRUD des Evaluations
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
