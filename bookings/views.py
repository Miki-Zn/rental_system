from rest_framework import viewsets, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel_booking(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user:
            return Response({"detail": "You cannot cancel someone else's booking."}, status=status.HTTP_403_FORBIDDEN)
        booking.delete()
        return Response({"detail": "Booking has been cancelled."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_booking(self, request, pk=None):
        booking = self.get_object()
        if booking.listing.owner != request.user:
            return Response({"detail": "You are not authorized to confirm this booking."}, status=status.HTTP_403_FORBIDDEN)
        booking.is_confirmed = True
        booking.save()
        return Response({"detail": "Booking has been confirmed."})
