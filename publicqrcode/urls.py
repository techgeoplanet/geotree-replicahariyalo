from django.urls import path
from .views import qrid_view

urlpatterns = [
    path('qrid/', qrid_view, name='qrid'),  # Accepts both string and numeric IDs
]
