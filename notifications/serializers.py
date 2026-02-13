from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    # Add these custom fields to display user information
    user_name = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='object_id', read_only=True)
    user_type = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'user_name', 'user_type', 'message', 
                  'type', 'is_read', 'created_at']
        read_only_fields = ['created_at', 'user_id', 'user_name', 'user_type']
    
    def get_user_name(self, obj):
        """Get the name of the user (Etudiant or Encadreur)"""
        try:
            user = obj.user
            if user:
                # Try to get nom and prenom (for Etudiant or Encadreur)
                if hasattr(user, 'nom'):
                    prenom = getattr(user, 'prenom', '')
                    return f"{user.nom} {prenom}".strip()
                return str(user)
        except:
            pass
        return "Unknown User"