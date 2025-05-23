from django.db import models
from django.conf import settings
from django.db.models import Avg

class Listing(models.Model):
    TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        result = self.listing_reviews.aggregate(avg=Avg('rating'))
        return result['avg'] or 0


class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name='listing_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('listing', 'user')

    def __str__(self):
        return f'{self.rating} by {self.user} on {self.listing}'
