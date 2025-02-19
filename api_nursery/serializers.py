from rest_framework import serializers
from .models import District, Block, GramPanchayat, Plant_List, NurseryDetails, ListOfPlantsInNursery

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('District_id', 'District_name')

    def create(self, validated_data):
        if isinstance(validated_data, list):  # Bulk creation
            return District.objects.bulk_create([District(**item) for item in validated_data])
        return super().create(validated_data)


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('block_id', 'block_name')

    def create(self, validated_data):
        if isinstance(validated_data, list):  # Bulk creation
            return Block.objects.bulk_create([Block(**item) for item in validated_data])
        return super().create(validated_data)


class GramPanchayatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GramPanchayat
        fields = ('gp_id', 'gp_name')

    def create(self, validated_data):
        if isinstance(validated_data, list):  # Bulk creation
            return GramPanchayat.objects.bulk_create([GramPanchayat(**item) for item in validated_data])
        return super().create(validated_data)


class PlantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_List
        fields = ('Plant_id', 'Plant_Name_hindi', 'Plant_Name')

    def create(self, validated_data):
        if isinstance(validated_data, list):  # Bulk creation
            return Plant_List.objects.bulk_create([Plant_List(**item) for item in validated_data])
        return super().create(validated_data)


class NurseryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseryDetails
        fields = '__all__'


class ListOfPlantsInNurserySerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOfPlantsInNursery
        fields = '__all__'
