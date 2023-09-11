# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Create a DefaultRouter instance
# router = DefaultRouter()

# # Register the UserProfileViewSet with the router, creating URL patterns
# router.register(r'profile', UserProfileViewSet)
urlpatterns = [
    path('signup/', views.CustomUserRegistration.as_view(), name='register'),
    # path('profile/', UserProfile.as_view(), name='profile'),
    path('create-profile/<str:username>/', views.UserProfileCreateView.as_view(), name='create-profile'),
    path('update-profile/<int:pk>/', views.UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('login/', views.CustomUserLogin.as_view(), name='login'),
]
