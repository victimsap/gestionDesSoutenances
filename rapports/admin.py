from django.contrib import admin
from .models import Rapport

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('sujet','uploaded_by','uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('sujet__title','uploaded_by__email','uploaded_by__username')
