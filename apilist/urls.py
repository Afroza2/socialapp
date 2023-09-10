from django.urls import path
from .views import SignupView, LoginView, UserProfileCreateView, UserProfileDetailView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # path('profile/', UserProfileView.as_view(), name='profile-view'),
    path('create/', UserProfileCreateView.as_view(), name='create-profile'),
    path('profile/<str:user>/', UserProfileDetailView.as_view(), name='profile-detail'),
]
