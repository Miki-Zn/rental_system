from rest_framework import viewsets, permissions, filters as drf_filters
from django_filters import rest_framework as django_filters
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from .serializers import ListingSerializer
from .forms import ListingForm



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
    filter_backends = (django_filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter)
    filterset_class = ListingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/list.html', {'listings': listings})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # request.user точно будет User
            listing.save()
            return redirect('listings:listing-list')
    else:
        form = ListingForm()
    return render(request, 'listings/create.html', {'form': form})



def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings:listing-list')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/update.html', {'form': form})

def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        return HttpResponseForbidden("You are not the owner of this listing.")

    if request.method == 'POST':
        listing.delete()
        return redirect('listings:listing-list')
    return render(request, 'listings/delete.html', {'listing': listing})
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/detail.html', {'listing': listing})

def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
