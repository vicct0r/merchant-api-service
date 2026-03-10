from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('me/', views.CustomUserRetrieveAPIView.as_view(), name='profile'),
    path('signup/', views.CustomUserCreateAPIView.as_view(), name='signup'),
]