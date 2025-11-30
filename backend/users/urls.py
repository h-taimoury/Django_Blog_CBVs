from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    UserListView,
    UserDetailView,
    UserProfileView,
)

urlpatterns = [
    # 1. User Registration (POST /register/)
    path("register/", UserRegistrationView.as_view(), name="register"),
    # 2. Login (Uses Simple JWT's built-in CBV)
    path("login/", TokenObtainPairView.as_view(), name="login"),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 3. User Profile (GET, PUT, PATCH, DELETE /me/)
    path("me/", UserProfileView.as_view(), name="me"),
    # 4. List All Users (GET /)
    path("", UserListView.as_view(), name="users"),
    # 5. User Detail (GET, PUT, PATCH, DELETE /<int:pk>/)
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
