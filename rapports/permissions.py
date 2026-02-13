from rest_framework import permissions

class IsUploaderOrRelatedOrAdmin(permissions.BasePermission):
    """
    Permission pour les rapports :
    - Admin : accès total
    - Uploadeur : peut modifier/supprimer son rapport
    - Étudiant/Encadreur lié au sujet : lecture seule
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.is_superuser:
            return True
        
        # Lecture seule pour tous les authentifiés liés
        if request.method in permissions.SAFE_METHODS:
            # L'uploadeur peut lire
            if obj.uploaded_by == request.user:
                return True
            # L'étudiant du sujet peut lire
            if hasattr(obj.sujet, 'etudiant') and obj.sujet.etudiant == request.user:
                return True
            # L'encadreur du sujet peut lire
            if hasattr(obj.sujet, 'encadreur') and obj.sujet.encadreur == request.user:
                return True
            return False
        
        # Modification/Suppression : seulement uploadeur ou admin
        return obj.uploaded_by == request.user