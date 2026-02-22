from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    # lembrar de buscar forma melhor de mapear as rotas
    # merchants_app esta com dominio: workplace + merchants
    path('v1/', include('merchants.urls')),
    path('v1/orders/', include('orders.urls')),
    path('v1/clients/', include('clients.urls')),
    path('v1/products/', include('products.urls')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]