from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title="Demo for interview BN",
        default_version='v1',
        description="API for interview BN",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="ntdung2508@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('user.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)