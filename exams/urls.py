from django.urls import path

from .views import ExamListView

urlpatterns = [
    path('<int:batch_year>/<str:class_name>/', ExamListView.as_view(), name='exams'),
]