from rest_framework import serializers
from .models import Etudiant, Encadreur, Sujet, Soutenance


class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'matricule', 'filiere']


class EncadreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encadreur
        fields = ['id', 'nom', 'prenom', 'specialite']


class SujetSerializer(serializers.ModelSerializer):
    etudiant = EtudiantSerializer(read_only=True)
    etudiant_id = serializers.PrimaryKeyRelatedField(
        queryset=Etudiant.objects.all(), write_only=True, source='etudiant'
    )

    encadreur = EncadreurSerializer(read_only=True)
    encadreur_id = serializers.PrimaryKeyRelatedField(
        queryset=Encadreur.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
        source='encadreur'
    )

    class Meta:
        model = Sujet
        fields = [
            'id', 'titre', 'description',
            'etudiant', 'etudiant_id',
            'encadreur', 'encadreur_id'
        ]


class SoutenanceSerializer(serializers.ModelSerializer):
    sujet = SujetSerializer(read_only=True)
    sujet_id = serializers.PrimaryKeyRelatedField(
        queryset=Sujet.objects.all(),
        write_only=True,
        source='sujet'
    )

    class Meta:
        model = Soutenance
        fields = [
            'id', 'sujet', 'sujet_id', 'date',
            'salle', 'jury', 'final_grade',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['final_grade', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Empêcher plusieurs soutenances pour un sujet."""
        sujet = attrs.get('sujet')

        # Cas création : self.instance est None
        if self.instance is None:
            if Soutenance.objects.filter(sujet=sujet).exists():
                raise serializers.ValidationError({
                    "sujet_id": "Ce sujet possède déjà une soutenance."
                })
        else:
            # Cas modification : empêcher changement vers un sujet déjà utilisé
            if sujet != self.instance.sujet:
                if Soutenance.objects.filter(sujet=sujet).exists():
                    raise serializers.ValidationError({
                        "sujet_id": "Ce sujet possède déjà une soutenance."
                    })

        return attrs
