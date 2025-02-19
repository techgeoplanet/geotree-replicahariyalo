from django.urls import path
from . import views

urlpatterns = [
    path('hi/update-plant/', views.updateIndivisualPlant, name='hiupdate-plant'),
    path('hi/map-validation/', views.mapValidation, name='himap-validation'),
    path('hi/aliveplant/', views.updateAlivePlant, name='hialiveplant'),
    path('hi/plantgallery/', views.plantgallery, name='hiplantgallery'),
    path('hi/updatedistrictfirst',views.updateDistrict, name='hiupdatedistrictfirst'),
]
