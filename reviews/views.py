from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from users.permissions import IsOwnerOrAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user', 'listing', 'booking')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        listing_id = self.request.query_params.get('listing')
        if listing_id:
            queryset = queryset.filter(listing__id=listing_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        booking = serializer.validated_data.get('booking')
        serializer.save(user=self.request.user, listing=booking.listing)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
