from django.db.models import Count
from rest_framework import views, response
from .models import SearchHistory, ViewHistory
from .serializers import PopularSearchSerializer, PopularListingSerializer

class PopularSearchesView(views.APIView):
    def get(self, request):
        data = SearchHistory.objects.values('keyword').annotate(count=Count('id')).order_by('-count')[:10]
        return response.Response(PopularSearchSerializer(data, many=True).data)

class PopularListingsView(views.APIView):
    def get(self, request):
        data = ViewHistory.objects.values('listing').annotate(count=Count('id')).order_by('-count')[:10]
        return response.Response(PopularListingSerializer(data, many=True).data)
