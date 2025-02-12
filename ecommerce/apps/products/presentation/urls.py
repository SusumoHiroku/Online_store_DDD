from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.presentation.views import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]