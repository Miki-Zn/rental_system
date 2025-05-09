from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Listing
from .serializers import ListingSerializer

class ListingFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')
    min_rooms = filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    max_rooms = filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    property_type = filters.ChoiceFilter(choices=Listing.TYPE_CHOICES)

    class Meta:
        model = Listing
        fields = ['min_price', 'max_price', 'location', 'min_rooms', 'max_rooms', 'property_type']

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
