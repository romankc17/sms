from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views.accounts import RegisterView, CustomTokenObtainPairView

from .views.teachers import TeacherView
from .views.students import StudentView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    # Generating token
    path('login/',CustomTokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Teacher
    path('teachers/', TeacherView.as_view(), name='teachers'),
    path('teachers/teacher/<int:teacher_id>/', TeacherView.as_view(), name='teacher'),

    # Student
    path('students/', StudentView.as_view(), name='students'),
    path('students/student/<int:student_id>/', StudentView.as_view(), name='student'),
]