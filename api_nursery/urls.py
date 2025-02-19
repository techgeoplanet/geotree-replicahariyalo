from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    DistrictViewSet,
    BlockViewSet,
    GramPanchayatViewSet,
    PlantListViewSet,
    NurseryDetailsViewSet,
    ListOfPlantsInNurseryViewSet,
    nurserydashview,
    districtListView,
    blockListView,
    gpListView,
    downloadNurceryDataFull,
)

router = DefaultRouter()
router.register('districts', DistrictViewSet)
router.register('blocks', BlockViewSet)
router.register('gram-panchayats', GramPanchayatViewSet)
router.register('plants', PlantListViewSet)
router.register('nurseries', NurseryDetailsViewSet)
router.register('nursery-plants', ListOfPlantsInNurseryViewSet)

urlpatterns = [
    path('nurserydash/', nurserydashview.view, name='nurserydash'),
    path('districtlist/', districtListView, name='districtlist'),
    path('blocklist/', blockListView, name='blocklist'),
    path('gplist/', gpListView, name='gplist'),
    path('downloadnurserydata/', downloadNurceryDataFull, name='downloadnurserydata'),

] + router.urls
