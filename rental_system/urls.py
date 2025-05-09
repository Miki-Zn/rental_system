from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from users.views import UserListView

router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', UserListView.as_view(), name='user-list'),
]

