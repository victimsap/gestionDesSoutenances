from rest_framework.routers import DefaultRouter
from .views import RapportViewSet

router = DefaultRouter()
router.register(r'rapports', RapportViewSet, basename='rapport')

urlpatterns = router.urls
