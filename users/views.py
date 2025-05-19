from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
