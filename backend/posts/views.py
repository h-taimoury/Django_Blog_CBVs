from rest_framework import generics, viewsets, permissions
from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostWriteSerializer,
    CommentSerializer,
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin


# ======================================================================
# 1. Post ViewSet (Replaces post_list_create and post_detail FBVs)
# ======================================================================


class PostViewSet(viewsets.ModelViewSet):
    """
    Handles all CRUD operations for Posts, with custom logic for
    queryset filtering, serialization, and response formatting.
    """

    # Permission applies to all actions in the ViewSet
    permission_classes = [IsAdminOrReadOnly]

    # ------------------
    # A. Custom Queryset Logic
    # ------------------
    # Handles complex logic: public vs. admin filtering + database optimization.
    def get_queryset(self):
        # 1. Base Queryset Filtering (Admin vs. Public)
        if self.request.user.is_staff:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(is_published=True)

        # 2. Optimization based on Action (replaces the 'if request.method == "GET":' logic)
        if self.action == "list":
            # Optimization for list view
            return queryset.select_related("author").order_by("-created_at")

        if self.action == "retrieve":
            # Optimization for detail view (includes comments)
            return queryset.select_related("author").prefetch_related(
                "comment_set__author"
            )

        # Default minimal queryset for write operations (create, update, destroy)
        return queryset

    # ------------------
    # B. Custom Serializer Logic
    # ------------------
    # Handles selection of Read vs. Write serializers.
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer  # default for 'list'

    # ------------------
    # C. Custom Create/Update Logic
    # ------------------
    def perform_create(self, serializer):
        """Injects the author before saving the Post."""
        # This replaces the manual `serializer.save(author=request.user)`
        self.created_instance = serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """Overrides create to return the custom minimal success response."""
        response = super().create(request, *args, **kwargs)

        # Logic from the old FBV
        post_url = f"/posts/{self.created_instance.slug}-{self.created_instance.id}/"
        response.data = {
            "url": post_url,
            "message": "Post created successfully.",
        }
        return response

    def update(self, request, *args, **kwargs):
        """Overrides update/patch to return the custom minimal success response."""
        response = super().update(request, *args, **kwargs)
        # Logic from the old FBV
        response.data = {"message": "Post updated successfully."}
        return response

    partial_update = update  # Use the same method for PATCH


# ======================================================================
# 2. Comment Generics (Replaces comment_create and comment_detail FBVs)
# ======================================================================


class CommentCreateView(generics.CreateAPIView):
    """
    Handles POST requests to create a new comment.
    Replaces the comment_create FBV.
    """

    queryset = Comment.objects.all()  # Used for internal model reference
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Replaces the manual author injection
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET, PUT, PATCH, DELETE requests for a single comment.
    Replaces the comment_detail FBV.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]

    # We only need to override perform_update to replicate the specific logic
    # that prevents non-admins from changing 'is_approved'.
    def perform_update(self, serializer):
        # If a non-admin is updating, ensure they cannot set is_approved=True
        if not self.request.user.is_staff:
            if "is_approved" in serializer.validated_data:
                del serializer.validated_data["is_approved"]

        serializer.save()

    # NOTE: The manual object-level permission check from the FBV is GONE!
    # The [IsAuthorOrAdmin] permission class and the RetrieveUpdateDestroyAPIView
    # automatically handle the has_object_permission check for us.
