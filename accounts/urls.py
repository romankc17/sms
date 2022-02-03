from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views.accounts import RegisterView, CustomTokenObtainPairView

from .views.teachers import TeacherView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('login/',CustomTokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('teachers/', TeacherView.as_view(), name='teachers'),
    path('teachers/teacher/<int:teacher_id>/', TeacherView.as_view(), name='teacher'),
]