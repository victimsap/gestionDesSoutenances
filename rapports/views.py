from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Rapport
from .serializers import RapportSerializer
from .permissions import IsUploaderOrRelatedOrAdmin

class RapportViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les rapports.
    - create: multipart/form-data (file + sujet)
    - list: admin voit tout; autres voient rapports liés à eux (uploads) et/ou rapports de leurs sujets
    - retrieve: permission objet
    """
    queryset = Rapport.objects.all().select_related('uploaded_by','sujet').order_by('-uploaded_at')
    serializer_class = RapportSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # list & create accessible aux authentifiés ; detail uses custom object permission
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsUploaderOrRelatedOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        # rapports que l'utilisateur a uploadés
        qs = Rapport.objects.filter(uploaded_by=user)
        # si l'utilisateur est encadreur ou étudiant, ajouter rapports liés à ses sujets
        qs2 = Rapport.objects.filter(sujet__student=user) | Rapport.objects.filter(sujet__encadreur=user)
        return (qs | qs2).distinct().order_by('-uploaded_at')

    def perform_create(self, serializer):
        # uploaded_by set in serializer.create but ensure here as well
        serializer.save(uploaded_by=self.request.user)
