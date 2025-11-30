from rest_framework import generics, permissions
from .serializers import UserSerializer, UserSerializerWithToken
from .models import User


# --- 1. User Registration (Replaces register_user FBV) ---
class UserRegistrationView(generics.CreateAPIView):
    """
    Handles user registration via POST request.
    Uses UserSerializerWithToken to return a token on creation.
    """

    queryset = User.objects.all()
    # Use the serializer that handles token creation in its save() method
    serializer_class = UserSerializerWithToken
    # Allow anyone to access the registration endpoint
    permission_classes = [permissions.AllowAny]

    # The CreateAPIView's perform_create method is called on serializer.save().
    # The default implementation calls serializer.save() which handles validation
    # and the custom create() logic in UserSerializerWithToken.


# --- 2. List All Users (Replaces get_users FBV) ---
class UserListView(generics.ListAPIView):
    """
    Handles GET request to list all users.
    Restricted to admin users (is_staff=True).
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    # Custom permission: IsAdminUser (from your FBV)
    permission_classes = [permissions.IsAdminUser]


# --- 3. User Detail, Update, Delete (Replaces user_detail FBV) ---
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, DELETE requests for a specific user by PK.
    Restricted to admin users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # The URL pattern provides the 'pk' argument, which is automatically handled by the CBV.
    permission_classes = [permissions.IsAdminUser]


# --- 4. User Profile (Replaces user_profile FBV) ---
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, DELETE requests for the currently logged-in user.
    """

    serializer_class = UserSerializer
    # Ensure only logged-in users can access this endpoint
    permission_classes = [permissions.IsAuthenticated]

    # Override get_object to fetch the currently authenticated user
    def get_object(self):
        # The request.user is set by the authentication system (Simple JWT)
        return self.request.user
