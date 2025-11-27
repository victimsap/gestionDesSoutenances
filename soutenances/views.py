from rest_framework import viewsets, permissions
from .models import Etudiant, Encadreur, Sujet, Soutenance
from .serializers import EtudiantSerializer, EncadreurSerializer, SujetSerializer, SoutenanceSerializer

class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EncadreurViewSet(viewsets.ModelViewSet):
    queryset = Encadreur.objects.all()
    serializer_class = EncadreurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SujetViewSet(viewsets.ModelViewSet):
    queryset = Sujet.objects.all().order_by('-id')
    serializer_class = SujetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class SoutenanceViewSet(viewsets.ModelViewSet):
    queryset = Soutenance.objects.all().order_by('-date')
    serializer_class = SoutenanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
