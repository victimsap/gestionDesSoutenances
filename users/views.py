from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, RegisterSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['role'] = user.role  # ajoute le rôle dans le token
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Identifiants invalides"}, status=400)

        tokens = get_tokens_for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        })


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"})
        except:
            return Response({"error": "Token invalide"}, status=400)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, RegisterSerializer


# Génération des tokens (access + refresh)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role  # ajoute le rôle dans le payload du token

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ============================
# REGISTER
# ============================
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({
                "message": "Inscription réussie.",
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================
# LOGIN
# ============================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Email ou mot de passe incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = get_tokens_for_user(user)

        return Response({
            "message": "Connexion réussie.",
            "user": UserSerializer(user).data,
            "tokens": tokens
        })


# ============================
# ME (profil utilisateur connecté)
# ============================
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data)


# ============================
# LOGOUT (blacklist du refresh token)
# ============================
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Déconnexion réussie."})

        except Exception:
            return Response({"error": "Token invalide ou déjà expiré."},
                            status=status.HTTP_400_BAD_REQUEST)
