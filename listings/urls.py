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


    path('list/', views.listing_list, name='listing_list'),
    path('create/', views.listing_create, name='listing_create'),
    path('update/<int:pk>/', views.listing_update, name='listing_update'),
    path('delete/<int:pk>/', views.listing_delete, name='listing_delete'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),

]
