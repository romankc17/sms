from django.urls import path

from .views import (
    BatchView,
    ClassView,
    SectionView,
)

urlpatterns = [
    path('batches/', BatchView.as_view(), name='batches'),
    path('batches/batch/<int:batch_year>/', BatchView.as_view(), name='batch'),

    # deleting a class
    path('batches/batch/<int:batch_year>/class/<str:class_name>/', ClassView.as_view(), name='class'),

    # deleting a section
    path('batches/batch/<int:batch_year>/class/<str:class_name>/section/<str:section_name>/', SectionView.as_view(), name='section'),
]
