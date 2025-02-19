# admin.py
from django.contrib import admin
from api.models import *
from portaldash.models import *
from rangefilter.filters import DateRangeFilter

class GovDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name')
    search_fields = ('department_name',)

class LandOwnershipByGovNgoAdmin(admin.ModelAdmin):
    list_display = ('id', 'land_ownership')
    search_fields = ('land_ownership',)

class PlantationByPvtAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantation_name', 'plantation_height', 'dict_code','block_code','gp_code','location_lat', 'location_long', 'submitted_by', 'status', 'created_at', 'updated_at','image1', 'image3')
    search_fields = ('plantation_name','submitted_by__phone','id','dict_code','block_code','gp_code',)
    list_filter = ('status', ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),'dict_code','block_code')
    readonly_fields = ('created_at', 'updated_at')

class PlantationByGovAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantation_name', 'plantation_height', 'dict_code','block_code','gp_code','gov_department_id', 'land_ownership', 'location_lat', 'location_long', 'submitted_by', 'status', 'created_at', 'updated_at','image1', 'image3')
    search_fields = ('plantation_name','submitted_by__phone','gov_department_id__department_name','id','dict_code','block_code','gp_code',)
    list_filter = ('status', ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),'gov_department_id__department_name' ,'dict_code','block_code')
    readonly_fields = ('created_at', 'updated_at')

class PlantationByNgoAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantation_name', 'plantation_height', 'dict_code','block_code','gp_code', 'ngo_name', 'land_ownership', 'location_lat', 'location_long', 'submitted_by', 'status', 'created_at', 'updated_at','image1', 'image3')
    search_fields = ('plantation_name','submitted_by__phone', 'ngo_name','id','dict_code','block_code','gp_code',)
    list_filter = ('status', ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),'dict_code','block_code','gp_code',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(gov_department, GovDepartmentAdmin)
admin.site.register(land_ownershipby_gov_ngo, LandOwnershipByGovNgoAdmin)
admin.site.register(plantation_bypvt, PlantationByPvtAdmin)
admin.site.register(plantation_bygov, PlantationByGovAdmin)
admin.site.register(plantation_byngo, PlantationByNgoAdmin)



# Register certificate_storage model
@admin.register(CertificateStorage)
class CertificateStorageAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'user_id', 'created_at')
    search_fields = ('certificate_id', 'user_id')
    readonly_fields = ['created_at']

# Register reward_storage model
@admin.register(reward_storage)
class RewardStorageAdmin(admin.ModelAdmin):
    list_display = ('plantation_id', 'created_at', 'updated_at')
    search_fields = ('plantation_id',)
    readonly_fields = ('created_at', 'updated_at')

# Register TempStorageCertificateInfo model
@admin.register(TempStorageCertificateInfo)
class TempStorageCertificateInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'plantation_id_bypvt', 'plantation_id_bygov', 'plantation_id_byngo', 'certificate_holder_name', 'certificate_id', 'created_at', 'updated_at')
    search_fields = ('user_id', 'certificate_holder_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OTP_model)
class OTPModelAdmin(admin.ModelAdmin):
    list_display = ['user_phone', 'otp', 'created_at', 'expiration_time']
    search_fields = ['user_phone', 'otp']  # Example search fields
    list_filter = ('created_at', 'expiration_time')
    
# If you don't want to customize the admin interface, you can simply register the models without custom admin classes:
# admin.site.register(certificate_storage)
# admin.site.register(reward_storage)
# admin.site.register(TempStorageCertificateInfo)

