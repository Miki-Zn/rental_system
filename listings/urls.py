from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from listings.views import ListingSearchView

app_name = 'listings'

router = DefaultRouter()
router.register(r'api/listings', views.ListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),

    path('search/', ListingSearchView.as_view(), name='listing-search'),

    path('list/', views.listing_list, name='listing_list'),
    path('create/', views.listing_create, name='listing_create'),
    path('update/<int:pk>/', views.listing_update, name='listing_update'),
    path('delete/<int:pk>/', views.listing_delete, name='listing_delete'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),


    path('<int:listing_pk>/reviews/<int:review_pk>/edit/', views.review_update, name='review_update'),
    path('<int:listing_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
]
