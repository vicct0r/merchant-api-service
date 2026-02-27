from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListCreateAPIView.as_view(), name='root'),
    path('active/', views.ClientListAPIView.as_view(), name='actives'),
    path('<uuid:id>/', views.ClientRetrieveUpdateDestroy.as_view(), name='retrieve')
]