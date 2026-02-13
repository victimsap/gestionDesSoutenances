from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationViewSet, index  # importer index
from . import views

# Router DRF pour l'API
router = DefaultRouter()
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

urlpatterns = router.urls
