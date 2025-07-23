from django.utils.html import format_html
from django.contrib import admin

# Register your models here.

from .models import Matiere, Document

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'display_color', 'icone')
    search_fields = ('nom',)
        
    def display_color(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {};'
            'display: inline-block; border: 1px solid #ddd;"></div> {}',
            obj.couleur,
            obj.couleur
        )
    display_color.short_description = 'Couleur'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'type_fichier', 'auteur', 'date_upload')
    list_filter = ('matiere', 'type_fichier', 'date_upload')
    search_fields = ('titre', 'auteur')
    readonly_fields = ('nombre_telechargements',)
    fieldsets = (
        (None, {
            'fields': ('titre', 'fichier', 'matiere')
        }),
        ('Détails', {
            'fields': ('type_fichier', 'auteur', 'nombre_telechargements')
        }),
    )