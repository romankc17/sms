from django.urls import path

from .views import (
    BatchView,
)

urlpatterns = [
    path('batches/', BatchView.as_view(), name='batches'),
]