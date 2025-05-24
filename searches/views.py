from rest_framework import generics, permissions
from .models import SearchHistory
from .serializers import SearchHistorySerializer
from django.db.models import Count


class SearchHistoryCreateView(generics.CreateAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PopularSearchesListView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return SearchHistory.objects.values('keyword').annotate(count=Count('keyword')).order_by('-count')[:10]

