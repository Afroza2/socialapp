# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.CustomUserRegistration.as_view(), name='register'),
    # path('profile/', UserProfile.as_view(), name='profile'),
    path('create-profile/<int:user_id>/', views.UserProfileCreateView.as_view(), name='create-profile'),
    path('update-profile/', views.UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('login/', views.CustomUserLogin.as_view(), name='login'),
    path('connect/<int:user_id>/', views.ConnectView.as_view(), name='connect'),
    path('connections/<int:user_id>/', views.ConnectionListView.as_view(), name='connections'),
    # path('connections/', views.ConnectionListView.as_view(), name='connections'),
    path('connections/remove/<int:user_id>/<int:friend_id>/', views.RemoveFriendView.as_view(), name='remove-friend'),
  
    path('feed/<int:user_id>/', views.UserFeedView.as_view(), name='user-feed'),
    path('posts/create/', views.CreatePostView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/like/', views.LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/comment/', views.CommentPostView.as_view(), name='comment-post'),
    path('posts/<int:post_id>/share/', views.SharePostView.as_view(), name='share-post'),
    path('posts/search/', views.SearchPostsView.as_view(), name='search-posts'),
]
