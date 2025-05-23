from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rental_system.views import home
from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from users.views import UserListView

# DRF Router
router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [

    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/list/', UserListView.as_view(), name='user-list'),
    path('api/users/', include(('users.urls', 'users'), namespace='users-api')),


    path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include(router.urls)),
    path('api/', include('searches.urls')),
    path('api/', include('bookings.urls')),

    path('listings/', include(('listings.urls', 'listings'), namespace='listings')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
