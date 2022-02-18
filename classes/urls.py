from django.urls import path

from .views import (
    BatchView,
    ClassView,
    SectionView,
)

urlpatterns = [
    path('batches/', BatchView.as_view(), name='batches'),
    path('batches/batch/<int:batch_year>/', BatchView.as_view(), name='batch'),

    # class
    path('batch/<int:batch_year>/class/<str:class_name>/', ClassView.as_view(), name='class'),
    path('batch/<int:batch_year>/classes/', ClassView.as_view(), name='class_list'),

    # section
    path('batch/<int:batch_year>/class/<str:class_name>/section/<str:section_name>/', 
            SectionView.as_view(), 
            name='section'
        ),
    path('batch/<int:batch_year>/class/<str:class_name>/sections/',
            SectionView.as_view(), 
            name='section_list'
        )
]
