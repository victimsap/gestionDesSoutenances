from rest_framework import serializers
from .models import Rapport
import os

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_file_extension(value):
    valid_extensions = ['.pdf']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise serializers.ValidationError("Seuls les fichiers PDF sont autorisés.")
    if value.size > MAX_FILE_SIZE:
        raise serializers.ValidationError("Le fichier est trop volumineux (max 10 MB).")
    return value

class RapportSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Rapport
        fields = ['id','sujet', 'soutenance', 'file','uploaded_by','uploaded_by_name','uploaded_at']
        read_only_fields = ['uploaded_by','uploaded_by_name','uploaded_at']

    def validate_file(self, value):
        return validate_file_extension(value)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)

    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}"
        return None


