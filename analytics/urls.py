from django.urls import path
from .views import PopularSearchesView, PopularListingsView

urlpatterns = [
    path('popular-searches/', PopularSearchesView.as_view(), name='popular-searches'),
    path('popular-listings/', PopularListingsView.as_view(), name='popular-listings'),
]
