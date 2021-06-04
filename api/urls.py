from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet, StoreViewSet, PendingStoreViewSet, TagViewSet

viewset_url = DefaultRouter()
viewset_url.register(r"products", ProductViewSet)
viewset_url.register(r"stores", StoreViewSet)
viewset_url.register(r"tags", TagViewSet)
viewset_url.register(r"pending_store", PendingStoreViewSet)

urlpatterns = [
    path("stores/propose", views.propose),
    path("stores/add", views.add),
    path(r"", include(viewset_url.urls))
]
