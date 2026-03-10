from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListCreateAPIView.as_view(), name='root'),
    path('logs/', views.ProductLogsListAPIView.as_view(), name='logs'),
]