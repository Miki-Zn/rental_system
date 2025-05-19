from rest_framework import viewsets, permissions, filters as drf_filters
from django_filters import rest_framework as django_filters
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Listing, Review
from .serializers import ListingSerializer
from .forms import ListingForm, ReviewForm


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    if listing.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this listing.")

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
    if listing.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this listing.")

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:listing_list')
    return render(request, 'listings/delete.html', {'listing': listing})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = Review.objects.filter(listing=listing).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to leave a review.")

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

    if review.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв.")

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

    if review.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот отзыв.")

    if request.method == 'POST':
        review.delete()
        return redirect('listings:listing_detail', pk=listing_pk)

    return render(request, 'listings/review_delete.html', {
        'review': review,
        'listing': listing,
    })
