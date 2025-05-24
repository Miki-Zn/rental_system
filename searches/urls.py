from django.urls import path
from .views import SearchHistoryCreateView, PopularSearchesListView

urlpatterns = [
    path('search-history/', SearchHistoryCreateView.as_view(), name='search-history-create'),
    path('popular-searches/', PopularSearchesListView.as_view(), name='popular-searches-list'),
    #path('view-history/', ViewHistoryListView.as_view(), name='view-history-list'),
]
