from rest_framework import serializers
from .models import Document, Matiere

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'couleur', 'icone']

class DocumentSerializer(serializers.ModelSerializer):
    matiere = MatiereSerializer(read_only=True)
    fichier_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'titre', 'fichier_url', 'matiere',
            'type_fichier', 'auteur', 'date_upload',
            'nombre_telechargements'
        ]
        read_only_fields = ['couleur'] 

    def get_fichier_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.fichier.url)