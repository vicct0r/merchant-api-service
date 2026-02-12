from django.urls import path
from . import views


urlpatterns = [
    path('', views.ClientListCreateAPIView.as_view()),
    path('active/', views.ClientListAPIView.as_view()),
    path('<uuid:id>/', views.ClientRetrieveUpdateDestroy.as_view())
]