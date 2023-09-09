from django.urls import path
from .views import SignupView, LoginView, UserProfileListCreateView, UserProfileDetailView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profiles/', UserProfileListCreateView.as_view(), name='profile-list-create'),
    # path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
]
