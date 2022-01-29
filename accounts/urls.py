from django.urls import path

from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('login/', 
         jwt_views.TokenObtainPairView.as_view(), 
         name='token_create'),  # override sjwt stock token
    path('token/refresh/', 
         jwt_views.TokenRefreshView.as_view(), 
         name='token_refresh'),
]