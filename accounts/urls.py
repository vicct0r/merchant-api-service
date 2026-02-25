from django.urls import path
from . import views


urlpatterns = [
    path('me/', views.CustomUserRetrieveAPIView.as_view()),
    path('signup/', views.CustomUserCreateAPIView.as_view()),
]