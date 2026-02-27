from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view(), name='root'),
    path('active/', views.AllOrdersListAPIView.as_view(), name='actives'),
    path('<uuid:id>/', views.OrderRetrieveUpdateDestroy.as_view(), name='retrieve'),
]