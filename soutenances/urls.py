from rest_framework.routers import DefaultRouter
from .views import EtudiantViewSet, EncadreurViewSet, SujetViewSet, SoutenanceViewSet

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'encadreurs', EncadreurViewSet, basename='encadreur')
router.register(r'sujets', SujetViewSet, basename='sujet')
router.register(r'soutenances', SoutenanceViewSet, basename='soutenance')

urlpatterns = router.urls
