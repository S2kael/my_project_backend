from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet

product_url = DefaultRouter()
product_url.register(r"products", ProductViewSet)

urlpatterns = [
    path("stores/propose", views.propose),
    path("stores/add", views.add),
    path(r"", include(product_url.urls))
]
