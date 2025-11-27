from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsEtudiant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "etudiant"


class IsEncadreur(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "encadreur"


class IsJury(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "jury"
