from django.contrib import admin
from django.urls import path, include

# The following import is here for drf_spectacular library
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# The following two imports are here for serving post images during development
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static function

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/posts/", include("posts.urls")),
    # The following two URL patterns are here for drf_spectacular library
    # API Schema View (The raw JSON/YAML specification file)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI View (The interactive documentation interface)
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# 💥 SERVE MEDIA FILES ONLY IN DEVELOPMENT 💥
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
