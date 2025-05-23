from django.db import models
from users.models import User
from listings.models import Listing
from bookings.models import Booking

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_reviews', null=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review', null=True, default=None)
    rating = models.IntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} - {self.listing.title}"

    def save(self, *args, **kwargs):
        if self.booking and not self.booking.is_confirmed:
            raise ValueError("Review can only be left for confirmed bookings.")
        super().save(*args, **kwargs)
