from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders.presentation.views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]