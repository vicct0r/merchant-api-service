from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view(), name='root'),
    path('active/', views.AllOrdersListAPIView.as_view(), name='actives'),
    path('<uuid:id>/', views.OrderRetrieveUpdateDestroy.as_view(), name='retrieve'),
    path('<uuid:order_id>/products/', views.OrderItemCreateAPIView.as_view(), name='add_product'),
    path('<uuid:order_id>/product/', views.OrderRetrieveUpdateDestroy.as_view(), name='order_product')
]