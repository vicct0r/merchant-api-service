from django.urls import path
from . import views

app_name = 'workplace'

urlpatterns = [
    path('workplace/', views.WorkplaceCreateAPIView.as_view(), name='root'),
    path('workplace/current/', views.WorkplaceGETAPIView.as_view(), name='get'),
    path('workplace/<uuid:id>/', views.WorkplacePublicAPIView.as_view(), name='retrieve'),
    path('workplace/join/', views.WorkplaceInvitationAPIView.as_view(), name='join'),
    path('workplace/update/', views.WorkplaceOwnerManagmentAPIView.as_view(), name='update'),
    path('workplace/update/member/', views.WorkplaceAddUserAPIView.as_view(), name='add_member')
]