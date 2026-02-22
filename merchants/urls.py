from django.urls import path
from . import views


urlpatterns = [
    path('workplace/', views.WorkplaceCreateAPIView.as_view()),
    path('workplace/join/<uuid:invite>/', views.JoinAsMerchantAPIView.as_view())
]