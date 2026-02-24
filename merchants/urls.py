from django.urls import path
from . import views


urlpatterns = [
    path('workplace/', views.WorkplaceCreateAPIView.as_view()),
    path('workplace/<uuid:id>/', views.WorkplacePublicAPIView.as_view()),
    path('workplace/join/', views.WorkplaceInvitationAPIView.as_view()),
    path('workplace/update/', views.WorkplaceOwnerManagmentAPIView.as_view()),
]