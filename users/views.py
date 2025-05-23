from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        role = self.request.data.get('role', 'user')
        user.role = role
        user.save()
        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        except Group.DoesNotExist:
            pass

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role') or 'user'
            user.save()
            try:
                group = Group.objects.get(name=user.role)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
            login(request, user)
            return redirect('listings:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
