from django.contrib import admin
from .models import *
from datetime import datetime
import csv
from django.http import HttpResponse
from portaldash.models import GpFinalList, BlockList, DistrictList


@admin.register(PlantationType)
class PlantationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantation_type_name')
    search_fields = ('plantation_type_name',)


@admin.action(description='Calculate total number of plants for selected rows')
def calculate_total_number_of_plants(modeladmin, request, queryset):
    total_plants = sum(int(item.number_of_plants) for item in queryset if item.number_of_plants.isdigit())
    modeladmin.message_user(request, f'Total number of plants: {total_plants}')

@admin.action(description='Download selected rows as CSV')
def download_as_csv(modeladmin, request, queryset):
    # Create an HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    current_date = datetime.now().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'attachment; filename=block_plantation_{current_date}.csv'
    
    writer = csv.writer(response)
    
    # Write the header
    writer.writerow(['ID', 'Submitted By','plantation_type', 'goverment_departmet', 'Image','DISTRICT_N','BLOCK_N','GP_FINAL_N', 'land_ownership', 'Location Latitude', 'Location Longitude', 'Number of Plants', 'Plantation Area in (Hec)', 'Location List', 'Status', 'Created At', 'Updated At'])
    
    # Write the data rows
    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.submitted_by.email,
            obj.plantation_type.plantation_type_name,
            obj.goverment_departmet.department_name,
            obj.image1_block_planation.url if obj.image1_block_planation else '',
            obj.dict_code,
            obj.block_code,
            obj.gp_code,
            obj.land_ownership.land_ownership,  # land_ownership.get_land_ownership_display()
            obj.location_lat,
            obj.location_long,
            obj.number_of_plants,
            obj.plantationArea,
            obj.location_list,
            obj.status,
            obj.created_at,
            obj.updated_at,
        ])
    
    return response

from rangefilter.filters import DateRangeFilter

@admin.register(BlockPlantation)
class BlockPlantationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'submitted_by', 'image1_block_planation', 'location_lat',
        'location_long', 'number_of_plants', 'plantationArea', 'dict_code','block_code','gp_code', 'location_list',
        'status', 'created_at', 'updated_at', 'goverment_departmet',
    )
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
        'goverment_departmet',
        'status',
        'plantationArea',
    )
    search_fields = (
        'submitted_by__email',
        'location_list',
        'number_of_plants',
        'planta_name_text',
        'dict_code__DISTRICT_N','block_code__BLOCK_N','gp_code__GP_FINAL_N',
        'created_at'
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = [calculate_total_number_of_plants, download_as_csv]

@admin.register(registration_role_department)
class RegistrationRoleDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reg_dep_name')
    search_fields = ('reg_dep_name',)
    list_filter = ('reg_dep_name',)

from .models import GovPlantationAdress, PvtPlantationAdress, NgoPlantationAdress, BlockPlantationAdress

@admin.register(PvtPlantationAdress)
class PvtPlantationAdressAdmin(admin.ModelAdmin):
    list_display = ('Plant_id_pvt', 'DISTRICT_C', 'BLOCK_CODE', 'GP_FINAL_C', 'created_at')

@admin.register(NgoPlantationAdress)
class NgoPlantationAdressAdmin(admin.ModelAdmin):
    list_display = ('Plant_id_ngo', 'DISTRICT_C', 'BLOCK_CODE', 'GP_FINAL_C', 'created_at')

@admin.register(BlockPlantationAdress)
class BlockPlantationAdressAdmin(admin.ModelAdmin):
    list_display = ('BlockPlantation', 'DISTRICT_C', 'BLOCK_CODE', 'GP_FINAL_C', 'created_at')

@admin.register(GovPlantationAdress)
class GovPlantationAdressAdmin(admin.ModelAdmin):
    list_display = ('Plant_id_gov', 'DISTRICT_C', 'BLOCK_CODE', 'GP_FINAL_C', 'created_at')
