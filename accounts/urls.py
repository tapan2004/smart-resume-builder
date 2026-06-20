from django.urls import path
from .views import AuthenticationAPIView

urlpatterns = [
    path('auth/', AuthenticationAPIView.as_view(), name='auth'),
]
