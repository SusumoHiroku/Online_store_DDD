from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reports.presentation.views import ReportViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
