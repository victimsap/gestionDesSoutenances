from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth (users app)
    path('api/auth/', include('users.urls')),  # Utilisation de users.urls à la place de authentication
    path('dashboard/', include('dashboard.urls')),
    path('soutenances/', include('soutenances.urls')),
    path('rapports/', include('rapports.urls')),
    path('evaluations/', include('evaluations.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
