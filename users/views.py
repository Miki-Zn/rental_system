from rest_framework import generics
from .models import User
from .serializers import UserSerializer, RegisterSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('listings:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
