from rest_framework import permissions

class IsUploaderOrRelatedOrAdmin(permissions.BasePermission):
    """
    Autorise l'accès si:
    - utilisateur est l'uploader
    - OU l'utilisateur est l'étudiant lié au sujet
    - OU l'utilisateur est l'encadreur du sujet
    - OU l'utilisateur est superuser (admin)
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # uploader
        if obj.uploaded_by == user:
            return True

        # étudiant lié au sujet
        try:
            if obj.sujet.student == user:
                return True
        except Exception:
            pass

        # encadreur du sujet
        try:
            if obj.sujet.encadreur == user:
                return True
        except Exception:
            pass

        return False
