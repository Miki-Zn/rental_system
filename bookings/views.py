from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsBookingOwner, IsListingOwner


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.none()  
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsBookingOwner])
    def cancel_booking(self, request, pk=None):
        booking = self.get_object()
        booking.delete()
        return Response({"detail": "Booking was successfully cancelled."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsListingOwner])
    def confirm_booking(self, request, pk=None):
        booking = self.get_object()
        if booking.is_confirmed:
            return Response({"detail": "Booking is already confirmed."}, status=status.HTTP_400_BAD_REQUEST)

        booking.is_confirmed = True
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
