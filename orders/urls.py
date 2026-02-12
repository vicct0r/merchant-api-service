from django.urls import path
from . import views


urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view()),
    path('active/', views.AllOrdersListAPIView.as_view()),
    path('<uuid:id>/', views.OrderRetrieveUpdateDestroy.as_view()),
]