from django.db import models
from users.models import User
from listings.models import Listing


class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name="bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.title} ({self.start_date} to {self.end_date})"

    class Meta:
        ordering = ['start_date']

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
