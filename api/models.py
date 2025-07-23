import random
from django.db import models

from django.db import models
import random

class Matiere(models.Model):
    # Liste de couleurs harmonieuses pour l'éducation
    PALETTE = [
        '#1565C0', '#2E7D32', '#D32F2F', '#F57C00', 
        '#7B1FA2', '#00796B', '#C2185B', '#512DA8',
        '#0288D1', '#689F38', '#E65100', '#5D4037'
    ]
    
    nom = models.CharField(max_length=100, unique=True)
    couleur = models.CharField(max_length=7, blank=True)
    icone = models.CharField(max_length=50, default='book')

    def __str__(self):
      return self.nom


    def save(self, *args, **kwargs):
        if not self.couleur:  # Seulement si la couleur n'est pas déjà définie
            self._assign_unique_color()
        super().save(*args, **kwargs)

    def _assign_unique_color(self):
        """Attribue une couleur non utilisée de la palette ou une aléatoire"""
        couleurs_utilisees = set(Matiere.objects.exclude(pk=self.pk)
                                .values_list('couleur', flat=True))
        
        # Trouve la première couleur disponible dans la palette
        for couleur in self.PALETTE:
            if couleur not in couleurs_utilisees:
                self.couleur = couleur
                return
        
        # Si toutes les couleurs sont utilisées, génère une couleur aléatoire
        self.couleur = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    
class Document(models.Model):
    TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('doc', 'Document Word'),
        ('img', 'Image'),
        ('ppt', 'Présentation'),
    ]

    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents/%Y/%m/%d/')
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True)
    type_fichier = models.CharField(max_length=10, choices=TYPE_CHOICES)
    auteur = models.CharField(max_length=100, default='Anonyme')
    date_upload = models.DateTimeField(auto_now_add=True)
    nombre_telechargements = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date_upload']
        indexes = [
            models.Index(fields=['-date_upload']),
            models.Index(fields=['matiere']),
        ]

    def __str__(self):
        return f"{self.titre} ({self.type_fichier})"