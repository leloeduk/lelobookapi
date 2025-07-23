from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'matieres', views.MatiereViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]