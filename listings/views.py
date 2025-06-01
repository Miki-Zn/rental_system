from rest_framework import viewsets, permissions, filters as drf_filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from analytics.models import ViewHistory
from listings.models import Listing, Review
from listings.serializers import ListingSerializer
from listings.forms import ListingForm, ReviewForm
from users.permissions import IsOwnerOrAdminOrReadOnly


class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    min_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='gte')
    max_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='lte')
    property_type = django_filters.ChoiceFilter(choices=Listing.TYPE_CHOICES)

    class Meta:
        model = Listing
        fields = ['min_price', 'max_price', 'location', 'min_rooms', 'max_rooms', 'property_type']


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    filter_backends = (
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    )
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_listings = Listing.objects.annotate(
            views_count=Count('viewhistory')
        ).order_by('-views_count')[:10]
        serializer = self.get_serializer(popular_listings, many=True)
        return Response(serializer.data)


def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/list.html', {'listings': listings})


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listings:listing_list')
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    user = request.user
    if listing.owner != user and getattr(user, 'role', None) != 'admin':
        raise PermissionDenied("You are not allowed to edit this listing.")

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:listing_detail', pk=pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/update.html', {'form': form, 'listing': listing})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    user = request.user
    if listing.owner != user and getattr(user, 'role', None) != 'admin':
        raise PermissionDenied("You are not allowed to delete this listing.")

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:listing_list')
    return render(request, 'listings/delete.html', {'listing': listing})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = Review.objects.filter(listing=listing).order_by('-created_at')

    ViewHistory.objects.create(
        user=request.user if request.user.is_authenticated else None,
        listing=listing
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to leave a review.")
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.user = request.user
            review.save()
            return redirect('listings:listing_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'listings/detail.html', {
        'listing': listing,
        'reviews': reviews,
        'form': form,
    })


@login_required
def review_update(request, listing_pk, review_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    review = get_object_or_404(Review, pk=review_pk, listing=listing)
    user = request.user

    if review.user != user and getattr(user, 'role', None) != 'admin':
        raise PermissionDenied("You do not have permission to edit this review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('listings:listing_detail', pk=listing_pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'listings/review_update.html', {
        'form': form,
        'listing': listing,
        'review': review,
    })


@login_required
def review_delete(request, listing_pk, review_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    review = get_object_or_404(Review, pk=review_pk, listing=listing)
    user = request.user

    if review.user != user and getattr(user, 'role', None) != 'admin':
        raise PermissionDenied("You do not have permission to delete this review.")

    if request.method == 'POST':
        review.delete()
        return redirect('listings:listing_detail', pk=listing_pk)

    return render(request, 'listings/review_delete.html', {
        'review': review,
        'listing': listing,
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listings:listing_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class ListingSearchView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        queryset = Listing.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
