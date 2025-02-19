from django import forms
from api.models import gov_department, land_ownershipby_gov_ngo, plantation_bypvt, plantation_bygov, plantation_byngo , TempStorageCertificateInfo

class GovDepartmentForm(forms.ModelForm):
    class Meta:
        model = gov_department
        fields = '__all__'

class LandOwnershipByGovNgoForm(forms.ModelForm):
    class Meta:
        model = land_ownershipby_gov_ngo
        fields = '__all__'

class PlantationByPvtForm(forms.ModelForm):
    class Meta:
        model = plantation_bypvt
        fields = ['plantation_name', 'plantation_height', 'location_lat', 'location_long','dict_code','block_code','gp_code', 'image1', 'image3']

class PlantationByGovForm(forms.ModelForm):
    class Meta:
        model = plantation_bygov
        fields = ['plantation_name', 'plantation_height', 'gov_department_id', 'land_ownership', 'location_lat', 'location_long','dict_code','block_code','gp_code', 'image1', 'image3']

class PlantationByNgoForm(forms.ModelForm):
    class Meta:
        model = plantation_byngo
        fields = ['plantation_name', 'plantation_height', 'ngo_name', 'land_ownership', 'location_lat', 'location_long','dict_code','block_code','gp_code', 'image1', 'image3']

class TempStorageCertificateInfoForm(forms.ModelForm):
    class Meta:
        model = TempStorageCertificateInfo
        fields = ['plantation_id_bypvt', 'plantation_id_bygov', 'plantation_id_byngo','selfi_image', 'certificate_holder_name']

# class PlantationPvtForm(forms.ModelForm):
#     class Meta:
#         model = plantation_bypvt
#         fields = ['plantation_name', 'plantation_height', 'location_lat', 'location_long', 'image1', 'image2', 'image3']

# class PlantationGovForm(forms.ModelForm):
#     class Meta:
#         model = plantation_bygov
#         fields = ['plantation_name', 'plantation_height', 'gov_department_id', 'land_ownership', 'location_lat', 'location_long', 'image1', 'image2', 'image3']

# class PlantationNgoForm(forms.ModelForm):
#     class Meta:
#         model = plantation_byngo
#         fields = ['plantation_name', 'plantation_height', 'ngo_name', 'land_ownership', 'location_lat', 'location_long', 'image1', 'image2', 'image3']
