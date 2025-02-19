from django.urls import path
from .views import *

urlpatterns = [
    path('portalmap/', portalmap_view, name='portalmap'),
    path('portaldash/', portaldash_view, name='portaldash'),
    path('departmentdatadash/', departmentdata_dash_view, name='departmentdatadash'),


    path('portalblockmap/', portalblockmap_view, name='portalblockmap'),
    path('portalblock/<str:id>/', portalblock_view, name='portalblock'),
    path('departmentdatablock/', departmentdata_block_view, name='departmentdatablock'),
    
    path('portalgpmap/', portalgpmap_view, name='portalgpmap'),
    path('portalgp/<str:id>/', portalgp_view, name='portalgp'),
    path('departmentdatagp/', departmentdata_gp_view, name='departmentdatagp'),

    path('gallery/', gallery_view, name='gallery_view'), 
    path("video-modal/", video_modal, name="video_modal"),

]