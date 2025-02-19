from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('mapcontent/', views.mapcontent, name='mapcontent'),
    path('mappolygon/', views.mappolygon, name='mappolygon'),
    path('GetCurrentLoactionAddresh/', views.GetCurrentLoactionAddresh, name='GetCurrentLoactionAddresh'),
]