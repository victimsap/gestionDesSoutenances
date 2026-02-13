from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/soutenances/', include('soutenances.urls')),
    path('api/rapports/', include('rapports.urls')),
    path('api/evaluations/', include('evaluations.urls')),
    path('notifications/', include('notifications.urls')),
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)