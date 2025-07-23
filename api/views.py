from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document, Matiere
from .serializers import DocumentSerializer, MatiereSerializer
from .pagination import DocumentPagination
from rest_framework.decorators import action
from rest_framework.response import Response

class MatiereViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom']

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all() 
    serializer_class = DocumentSerializer
    pagination_class = DocumentPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['matiere', 'type_fichier']
    search_fields = ['titre', 'auteur']
    ordering_fields = ['date_upload', 'nombre_telechargements']

    def get_queryset(self):
        return Document.objects.all().select_related('matiere')

    @action(detail=True, methods=['post'])
    def increment_download(self, request, pk=None):
        document = self.get_object()
        document.nombre_telechargements += 1
        document.save()
        return Response({'status': 'success'})