from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProductViewSet, TransactionViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet)
router.register("products", ProductViewSet)
router.register("transactions", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
