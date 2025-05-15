from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ListingViewSet,
    listing_list,
    listing_create,
    listing_update,
    listing_delete
)

app_name = 'listings'

router = DefaultRouter()
router.register(r'api/listings', ListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),



    path('list/', listing_list, name='list'),
    path('create/', views.listing_create, name='create'),
    path('create/', listing_create, name='listing-create'),
    path('update/<int:pk>/', listing_update, name='listing-update'),
    path('delete/<int:pk>/', listing_delete, name='listing-delete'),
]
