from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='reviews')

app_name = 'reviews'

urlpatterns = [
    path('', include(router.urls)),
]
