from django.urls import path
from . import views


urlpatterns = [
    path('', views.CustomUserCreateAPIView.as_view()),
]