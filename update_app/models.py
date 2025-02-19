from django.db import models
from django.conf import settings
from django.utils import timezone
from api_nursery.models import GramPanchayat
from api.models import land_ownershipby_gov_ngo, gov_department


# Another model for reference
class PlantHealthStatus(models.Model):
    id = models.AutoField(primary_key=True)
    health_status_en = models.CharField(max_length=255)
    health_status_hi = models.CharField(max_length=255)

# Abstract model for CenterIndividualPlantation
class CenterIndividualPlantationBase(models.Model):
    PLantid = models.CharField(primary_key=True, max_length=255)
    plant_name = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_gp_id = models.ForeignKey(
        GramPanchayat, on_delete=models.CASCADE, blank=True, null=True
    )
    land_ownership = models.ForeignKey(
        land_ownershipby_gov_ngo, on_delete=models.CASCADE, blank=True, null=True
    )
    imageurl_1 = models.CharField(max_length=500, blank=True, null=True)
    imageurl_2 = models.CharField(max_length=500, blank=True, null=True)
    submitted_by_user_id = models.ForeignKey(
        settings.AUTH_USERTEMP_MODEL, on_delete=models.CASCADE
    )
    submitted_by_department_id = models.ForeignKey(
        gov_department, on_delete=models.CASCADE, blank=True, null=True
    )
    submitted_by_ngo_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False)
    plant_alive_status = models.BooleanField(default=True)
    any_update_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Abstract model for UpdateData
class UpdateDataBase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USERTEMP_MODEL, on_delete=models.PROTECT
    )
    health_status = models.ForeignKey(
        'PlantHealthStatus', on_delete=models.PROTECT
    )
    Update_image1 = models.ImageField(upload_to="images/update_data/{version}/")
    height_infeet = models.DecimalField(max_digits=8, decimal_places=2)
    girth_infeet = models.DecimalField(max_digits=8, decimal_places=2)
    canopy_infeet = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status_date_mmyyyy = models.DateField(default=timezone.now)
    status_time = models.TimeField(default=timezone.now)

    class Meta:
        abstract = True


# Dynamic upload path
def upload_to_version(instance, filename):
    version = instance.__class__.__name__.split("_")[-1]  # Extract version from class name
    return f"images/update_data/{version}/{filename}"

# ------------------------------------------------------------------------------------------------

# Models for different versions
class CenterIndividualPlantation_99(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_100(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_101(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_102(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_103(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_104(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_105(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_106(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_107(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_108(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_109(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_110(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_111(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_112(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_113(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_114(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_115(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_116(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_117(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_118(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_119(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_120(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_121(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_122(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_123(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_124(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_125(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_126(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_127(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_128(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_129(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_130(CenterIndividualPlantationBase):
    pass


class CenterIndividualPlantation_131(CenterIndividualPlantationBase):
    pass


# -------------------------------------------------------------------------------

# Models for different versions
class UpdateData_99(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_99, on_delete=models.PROTECT, related_name="update_data99"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_100(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_100, on_delete=models.PROTECT, related_name="update_data100"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_101(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_101, on_delete=models.PROTECT, related_name="update_data101"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_102(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_102, on_delete=models.PROTECT, related_name="update_data102"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_103(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_103, on_delete=models.PROTECT, related_name="update_data103"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_104(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_104, on_delete=models.PROTECT, related_name="update_data104"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_105(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_105, on_delete=models.PROTECT, related_name="update_data105"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_106(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_106, on_delete=models.PROTECT, related_name="update_data106"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_107(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_107, on_delete=models.PROTECT, related_name="update_data107"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_108(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_108, on_delete=models.PROTECT, related_name="update_data108"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_109(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_109, on_delete=models.PROTECT, related_name="update_data109"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_110(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_110, on_delete=models.PROTECT, related_name="update_data110"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_111(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_111, on_delete=models.PROTECT, related_name="update_data111"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_112(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_112, on_delete=models.PROTECT, related_name="update_data112"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_113(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_113, on_delete=models.PROTECT, related_name="update_data113"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_114(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_114, on_delete=models.PROTECT, related_name="update_data114"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_115(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_115, on_delete=models.PROTECT, related_name="update_data115"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_116(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_116, on_delete=models.PROTECT, related_name="update_data116"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_117(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_117, on_delete=models.PROTECT, related_name="update_data117"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_118(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_118, on_delete=models.PROTECT, related_name="update_data118"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_119(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_119, on_delete=models.PROTECT, related_name="update_data119"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_120(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_120, on_delete=models.PROTECT, related_name="update_data120"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_121(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_121, on_delete=models.PROTECT, related_name="update_data121"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_122(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_122, on_delete=models.PROTECT, related_name="update_data122"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_123(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_123, on_delete=models.PROTECT, related_name="update_data123"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_124(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_124, on_delete=models.PROTECT, related_name="update_data124"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_125(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_125, on_delete=models.PROTECT, related_name="update_data125"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_126(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_126, on_delete=models.PROTECT, related_name="update_data126"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_127(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_127, on_delete=models.PROTECT, related_name="update_data127"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_128(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_128, on_delete=models.PROTECT, related_name="update_data128"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_129(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_129, on_delete=models.PROTECT, related_name="update_data129"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_130(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_130, on_delete=models.PROTECT, related_name="update_data130"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)


class UpdateData_131(UpdateDataBase):
    center_entry_plant = models.ForeignKey(
        CenterIndividualPlantation_131, on_delete=models.PROTECT, related_name="update_data131"
    )
    Update_image1 = models.ImageField(upload_to=upload_to_version)
