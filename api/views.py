# views.py
from rest_framework import viewsets
from .models import ConditionOpsations, OwnershipOpsations, TreeInfo, TreeImage, TreeData, PrivateOwnerShipDeatils, TempDatabase,TreeMoreDetails,PlaceDetails,TreeLocationsDetails
from .serializers import ConditionOpsationsSerializer, OwnershipOpsationsSerializer, TreeInfoSerializer, TreeImageSerializer, TreeDataSerializer, PrivateOwnerShipDeatilsSerializer,TempDatabaseSerializer,TreeMoreDetailsSerializer,PlaceDetailsSerializer,TreeLocationsDetailsSerializer
from .models import *
from .serializers import *


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsPatnerOrReadOnly
from account.renderers import UserRenderer
from rest_framework.exceptions import ValidationError,  MethodNotAllowed
from .utils import fetch_location_data

class ConditionOpsationsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]
    queryset = ConditionOpsations.objects.all()
    serializer_class = ConditionOpsationsSerializer

class OwnershipOpsationsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]
    queryset = OwnershipOpsations.objects.all()
    serializer_class = OwnershipOpsationsSerializer

class TreeInfoViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]
    queryset = TreeInfo.objects.all()
    serializer_class = TreeInfoSerializer

class TreeImageViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser,)
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = TreeImage.objects.all()
    serializer_class = TreeImageSerializer

class TreeDataViewSet(viewsets.ModelViewSet):
    # renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = TreeData.objects.all()
    serializer_class = TreeDataSerializer
    
    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)
        
class PrivateOwnerShipDeatilsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = PrivateOwnerShipDeatils.objects.all()
    serializer_class = PrivateOwnerShipDeatilsSerializer
    
class TempDatabaseViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = TempDatabase.objects.all()
    serializer_class = TempDatabaseSerializer
    
class TreeMoreDetailsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = TreeMoreDetails.objects.all()
    serializer_class = TreeMoreDetailsSerializer

class PlaceDetailsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = PlaceDetails.objects.all()
    serializer_class = PlaceDetailsSerializer

class TreeLocationsDetailsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly]
    queryset = TreeLocationsDetails.objects.all()
    serializer_class = TreeLocationsDetailsSerializer


class PlantationTypeViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]

    queryset = PlantationType.objects.all()
    serializer_class = PlantationTypeSerializer

class GovermentDepartmetViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]

    queryset = gov_department.objects.all()
    serializer_class = GovermentDepartmetSerializer

class LandOwnerShipViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]

    queryset = land_ownershipby_gov_ngo.objects.all()
    serializer_class = LandOwnerShipSerializer

class PlantViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer




from rest_framework.permissions import IsAuthenticated

from portaldash.signal import update_short_table

class BlockPlantationViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPatnerOrReadOnly, IsAuthenticated]
    queryset = BlockPlantation.objects.all()
    serializer_class = BlockPlantationSerializer

    def get_queryset(self):
        user = self.request.user
        return BlockPlantation.objects.filter(submitted_by=user)

    def perform_create(self, serializer):
        lat = self.request.data.get('location_lat')
        lon = self.request.data.get('location_long')
        number_of_plants = self.request.data.get('number_of_plants')

        if lat and lon:
            try:
                location_data = fetch_location_data(lat, lon)
                dict_code_id = location_data.get('dist_code', None)
                block_code_id = location_data.get('ps_code', None)
                gp_code_id = location_data.get('gp_code', None)

                # Fetch instances and handle the case where no instance is found
                dict_code = DistrictList.objects.filter(DISTRICT_C=dict_code_id).first()
                if dict_code is None:
                    dict_code = None  # Use None to indicate no match found
                
                block_code = BlockList.objects.filter(BLOCK_C=block_code_id).first()
                if block_code is None:
                    block_code = None  # Use None to indicate no match found
                
                gp_code = GpFinalList.objects.filter(GP_FINAL_C=gp_code_id).first()
                if gp_code is None:
                    gp_code = None  # Use None to indicate no match found

                instance = serializer.save(
                    submitted_by=self.request.user,
                    dict_code=dict_code,
                    block_code=block_code,
                    gp_code=gp_code
                )

                # Perform the update on ShortDatabase_normal if the save was successful
                if instance and gp_code_id:
                    update_short_table(GP_FINAL_C=gp_code_id, update_field='Total_block_plantation_Non_Verify_C', increment_value=number_of_plants)


            except Exception as e:
                print(f"Error fetching location data: {e}")
                # Save with default values if an exception occurs
                serializer.save(
                    submitted_by=self.request.user,
                    dict_code=None,
                    block_code=None,
                    gp_code=None
                )
        else:
            serializer.save(
                submitted_by=self.request.user,
                dict_code=None,
                block_code=None,
                gp_code=None
            )
        
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')