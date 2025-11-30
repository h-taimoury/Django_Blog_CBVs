from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Create Router for ViewSet
router = DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")

urlpatterns = [
    # ----------------------------------------------------------------------
    # 1. POST Endpoints (Handled by Router)
    # ----------------------------------------------------------------------
    # Maps to: /api/posts/ and /api/posts/<pk>/
    path("", include(router.urls)),
    # ----------------------------------------------------------------------
    # 2. COMMENT Endpoints (Handled by Generics)
    # ----------------------------------------------------------------------
    # Endpoint: /api/posts/comments/
    # Methods: POST
    path("comments/", views.CommentCreateView.as_view(), name="comment-create"),
    # ----------------------------------------------------------------------
    # Endpoint: /api/posts/comments/<int:pk>/
    # Methods: GET, PUT, PATCH and DELETE
    path(
        "comments/<int:pk>/",
        views.CommentDetailView.as_view(),
        name="comment-detail",
    ),
    # ----------------------------------------------------------------------
]
