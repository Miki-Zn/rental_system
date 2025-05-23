from django.db import models
from users.models import User
from listings.models import Listing


class SearchHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='searches',
        null=True, blank=True
    )
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Search: "{self.keyword}" by {self.user.username if self.user else "Anonymous"}'

    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = "Search History"


class ViewHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE,
        related_name='views'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f'{user_str} viewed "{self.listing.title}"'

    class Meta:
        ordering = ['-viewed_at']
        verbose_name_plural = "View History"
