from django.contrib import admin
from .models import District, Block, GramPanchayat, Plant_List, NurseryDetails, ListOfPlantsInNursery

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('District_id', 'District_name', 'created_at', 'updated_at')
    search_fields = ('District_name',)
    list_filter = ('created_at',)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('block_id', 'block_name', 'District', 'created_at', 'updated_at')
    search_fields = ('block_name', 'District__District_name')
    list_filter = ('District', 'created_at')


@admin.register(GramPanchayat)
class GramPanchayatAdmin(admin.ModelAdmin):
    list_display = ('gp_id', 'gp_name', 'block', 'District', 'created_at', 'updated_at')
    search_fields = ('gp_name', 'block__block_name', 'District__District_name')
    list_filter = ('block', 'District', 'created_at')


@admin.register(Plant_List)
class PlantListAdmin(admin.ModelAdmin):
    list_display = ('Plant_id', 'Plant_Name', 'Specis', 'created_at', 'updated_at')
    search_fields = ('Plant_Name', 'Specis')
    list_filter = ('created_at',)


@admin.register(NurseryDetails)
class NurseryDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'nursery_id', 
        'nursery_name', 
        'depart_id',
        'ownership' ,
        'total_quantity_of_plants', 
        'total_type_of_plants', 
        'status', 
        'gram_panchayat', 
        'submitted_by', 
        'submitted_date',
    )
    list_filter = ('status', 'location_filling', 'depart_id__department_name','ownership', 'gram_panchayat', 'submitted_date')
    search_fields = ('nursery_name', 'asfs_no', 'khasra_no')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-submitted_date',)


@admin.register(ListOfPlantsInNursery)
class ListOfPlantsInNurseryAdmin(admin.ModelAdmin):
    list_display = ('NurseryId', 'plant_id', 'NameOfPlant', 'quantity_of_plants', 'created_at', 'updated_at')
    search_fields = ('NurseryId__gram_panchayat__gp_name', 'NameOfPlant', 'plant_id__Plant_Name')
    list_filter = ('NurseryId', 'plant_id', 'created_at')
