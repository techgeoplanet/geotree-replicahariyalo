from django.contrib import admin
from .models import DistrictList, BlockList, GpFinalList ,ShortDatabase_chart ,ShortDatabase_deTable ,SiteVisitCount, TotalNumberOfPlantations, ShortDatabase_normal

@admin.register(DistrictList)
class DistrictListAdmin(admin.ModelAdmin):
    list_display = ('DISTRICT_C', 'DISTRICT_N')
    search_fields = ('DISTRICT_C', 'DISTRICT_N')
    list_filter = ('DISTRICT_N',)

@admin.register(BlockList)
class BlockListAdmin(admin.ModelAdmin):
    list_display = ('BLOCK_C', 'BLOCK_N')
    search_fields = ('BLOCK_C', 'BLOCK_N')
    list_filter = ('BLOCK_N',)

@admin.register(GpFinalList)
class GpFinalListAdmin(admin.ModelAdmin):
    list_display = ('GP_FINAL_C', 'GP_FINAL_N')
    search_fields = ('GP_FINAL_C', 'GP_FINAL_N')
    list_filter = ('GP_FINAL_N',)


@admin.register(ShortDatabase_chart)
class ShortDatabaseChartAdmin(admin.ModelAdmin):
    list_display = ('unique_id_code', 'value', 'date')
    list_filter = ('date', 'unique_id_code')
    search_fields = ('unique_id_code',)


@admin.register(ShortDatabase_deTable)
class ShortDatabase_deTableAdmin(admin.ModelAdmin):
    list_display = ('unique_id_code', 'department_name', 'value', 'date')
    list_filter = ('date', 'department_name')
    search_fields = ('unique_id_code', 'department_name')

@admin.register(SiteVisitCount)
class SiteVisitCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'SiteVisitCount')

@admin.register(TotalNumberOfPlantations)
class TotalNumberOfPlantationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'TotalPlantations')

class ShortDatabase_normalAdmin(admin.ModelAdmin):
    # Specify the fields for search functionality
    search_fields = (
        'DISTRICT_C', 'DISTRICT_N', 
        'BLOCK_C', 'BLOCK_N', 
        'GP_FINAL_C', 'GP_FINAL_N'
    )
    
    # Specify the fields for filtering in the admin interface
    list_filter = (
        'DISTRICT_N', 
        'BLOCK_N', 
        'GP_FINAL_N'
    )
    
    # Specify which fields to display in the list view
    list_display = (
        'DISTRICT_C', 'DISTRICT_N', 
        'BLOCK_C', 'BLOCK_N', 
        'GP_FINAL_C', 'GP_FINAL_N',
        'Total_Tag_Tree_Verify_C', 'Total_Tag_Tree_Non_Verify_C',
        'Total_block_plantation_Verify_C', 'Total_block_plantation_Non_Verify_C'
    )
    
    # Specify fields that should be read-only
    readonly_fields = (
        'Total_Tag_Tree_Verify_C', 'Total_Tag_Tree_Non_Verify_C',
        'Total_block_plantation_Verify_C', 'Total_block_plantation_Non_Verify_C'
    )

admin.site.register(ShortDatabase_normal, ShortDatabase_normalAdmin)