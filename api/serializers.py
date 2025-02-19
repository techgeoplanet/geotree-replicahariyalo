# serializers.py
from rest_framework import serializers
from .models import ConditionOpsations, OwnershipOpsations, TreeInfo, TreeImage, TreeData, PrivateOwnerShipDeatils,TempDatabase,TreeMoreDetails,PlaceDetails,TreeLocationsDetails
from .models import *
from portaldash.models import DistrictList, BlockList, GpFinalList

class ConditionOpsationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionOpsations
        fields = '__all__'

class OwnershipOpsationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnershipOpsations
        fields = '__all__'

class TreeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeInfo
        fields = '__all__'

class TreeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeImage
        fields = '__all__'

class TreeDataSerializer(serializers.ModelSerializer):
    TreeImage_id = TreeImageSerializer(read_only=True)
    TreeImage_id_by = serializers.PrimaryKeyRelatedField(queryset=TreeImage.objects.all(), source='TreeImage_id', write_only=True)
    
    TreeInfo_Id = TreeInfoSerializer(read_only=True)
    TreeInfo_Id_by = serializers.PrimaryKeyRelatedField(queryset=TreeInfo.objects.all(), source='TreeInfo_Id', write_only=True)
    
    ConditionInfo_id = ConditionOpsationsSerializer(read_only=True)
    ConditionInfo_id_by = serializers.PrimaryKeyRelatedField(queryset=ConditionOpsations.objects.all(), source='ConditionInfo_id', write_only=True)
    
    ownershipinfo_id = OwnershipOpsationsSerializer(read_only=True)
    ownershipinfo_id_by = serializers.PrimaryKeyRelatedField(queryset=OwnershipOpsations.objects.all(), source='ownershipinfo_id', write_only=True)
    
    class Meta:
        model = TreeData
        fields = ['QrCode', 'TreeImage_id', 'TreeInfo_Id', 'Girth_m', 'Height_m', 'Age_y',
                  'TreeCanopy_m', 'Location_Lat', 'Location_Long', 'Remarks', 'submitted_by',
                  'ConditionInfo_id', 'ownershipinfo_id','TreeImage_id_by','TreeInfo_Id_by','ConditionInfo_id_by','ownershipinfo_id_by']
        
class PrivateOwnerShipDeatilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateOwnerShipDeatils
        fields = '__all__'


class TempDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempDatabase
        fields = '__all__'

class TreeMoreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeMoreDetails
        fields = '__all__'

class PlaceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceDetails
        fields = '__all__'

class TreeLocationsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeLocationsDetails
        fields = '__all__'

class PlantationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantationType
        fields = '__all__'

class GovermentDepartmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = gov_department
        fields = '__all__'

class LandOwnerShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = land_ownershipby_gov_ngo
        fields = '__all__'


class BlockPlantationSerializer(serializers.ModelSerializer):
    submitted_by = serializers.ReadOnlyField(source='submitted_by.username')
    
    # Define related fields with queryset and default to None if not provided
    dict_code = serializers.PrimaryKeyRelatedField(queryset=DistrictList.objects.all(), required=False, allow_null=True)
    block_code = serializers.PrimaryKeyRelatedField(queryset=BlockList.objects.all(), required=False, allow_null=True)
    gp_code = serializers.PrimaryKeyRelatedField(queryset=GpFinalList.objects.all(), required=False, allow_null=True)

    class Meta:
        model = BlockPlantation
        fields = [
            'id',
            'submitted_by',
            'plantation_type',
            'goverment_departmet',
            'land_ownership',
            'location_list',
            'image1_block_planation',
            'location_lat',
            'location_long',
            'number_of_plants',
            'planta_name_text',
            'plantationArea',
            'status',
            'created_at',
            'updated_at',
            'dict_code',
            'block_code',
            'gp_code'
        ]

    def validate(self, data):
        """
        Ensure that `dict_code`, `block_code`, and `gp_code` are either valid objects or `None`.
        """
        if 'dict_code' in data and data['dict_code'] is None:
            raise serializers.ValidationError({"dict_code": "Invalid district code."})
        if 'block_code' in data and data['block_code'] is None:
            raise serializers.ValidationError({"block_code": "Invalid block code."})
        if 'gp_code' in data and data['gp_code'] is None:
            raise serializers.ValidationError({"gp_code": "Invalid GP code."})
        
        return data

    def create(self, validated_data):
        """
        Create a new BlockPlantation instance with the validated data.
        """
        return BlockPlantation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing BlockPlantation instance with the validated data.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

        
class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'name', 'synonyms', 'hindi_name', 'image']