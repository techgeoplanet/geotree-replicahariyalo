# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'conditionoptions', ConditionOpsationsViewSet)
router.register(r'ownershipoptions', OwnershipOpsationsViewSet)
router.register(r'treeinfo', TreeInfoViewSet)
router.register(r'treeimage', TreeImageViewSet)
router.register(r'treedata', TreeDataViewSet)
router.register(r'PrivateOwnerShipDeatils',PrivateOwnerShipDeatilsViewSet )
router.register(r'TempDatabase',TempDatabaseViewSet)
router.register(r'TreeMoreDetails',TreeMoreDetailsViewSet )
router.register(r'PlaceDetails',PlaceDetailsViewSet )
router.register(r'TreeLocationsDetails',TreeLocationsDetailsViewSet )


router.register(r'BlockPlantationAdd',BlockPlantationViewSet)

router.register(r'PlantationType',PlantationTypeViewSet )
router.register(r'LandOwnerShip',LandOwnerShipViewSet )
router.register(r'Plant',PlantViewSet )

router.register(r'GovermentDepartmet',GovermentDepartmetViewSet )

urlpatterns = [
    path('', include(router.urls)),
]
