from django.db import models
from django.utils import timezone
from datetime import timedelta
from account.models import TempUser ,User
from portaldash.models import DistrictList , BlockList , GpFinalList
import uuid
import os
# Create your models here.

class ConditionOpsations(models.Model):
    Condition = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
      return self.Condition

class OwnershipOpsations(models.Model):
    ownership = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
      return self.ownership

class TreeInfo(models.Model):
    TreeName = models.CharField(max_length=50)
    BotanicalName = models.CharField(max_length=50)
    Family = models.CharField(max_length=50)
    FlowerColor = models.CharField(max_length=20)
    FruitSeason = models.CharField(max_length=20)
    FlowerSeason = models.CharField(max_length=20)
    ShortDescription = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
      return self.TreeName


class TreeImage(models.Model):
    TreeImages =  models.ImageField(upload_to='images/' ,default=None, blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class TreeData(models.Model):
    QrCode = models.CharField(max_length=20,unique=True,primary_key=True)
    TreeImage_id = models.ForeignKey(TreeImage, on_delete=models.CASCADE, related_name="TreeImageUriBy")
    TreeInfo_Id = models.ForeignKey(TreeInfo,on_delete=models.CASCADE , related_name="TreeInfoBy")
    Girth_m = models.FloatField()
    Height_m = models.FloatField()
    Age_y = models.IntegerField()
    ConditionInfo_id = models.ForeignKey(ConditionOpsations, on_delete=models.CASCADE, related_name="ConditionBy")
    ownershipinfo_id = models.ForeignKey(OwnershipOpsations, on_delete=models.CASCADE, related_name="OwnershipBy")
    TreeCanopy_m = models.FloatField()
    Location_Lat = models.CharField(max_length=20)
    Location_Long = models.CharField(max_length=20)
    Remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
      return self.QrCode
  
class PrivateOwnerShipDeatils(models.Model):
    TreeData_id = models.ForeignKey(TreeData, on_delete=models.CASCADE, related_name="TreedataBy")
    Name = models.CharField(max_length=20, null=True, blank=True)
    Contact_number = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class TempDatabase(models.Model):
    TreeInfo_id = models.ForeignKey(TreeInfo, on_delete=models.CASCADE, related_name="TreeInfoFortemp")
    TreeImage_id = models.ForeignKey(TreeImage, on_delete=models.CASCADE, related_name="TreeImageUriByIntemp")
    Village_Name = models.CharField(max_length=30)
    ConditionInfo_id = models.ForeignKey(ConditionOpsations, on_delete=models.CASCADE, related_name="ConditionByIntemp")
    OwnershipInfo_id = models.ForeignKey(OwnershipOpsations, on_delete=models.CASCADE, related_name="OwnershipByIntemp")
    Plant_Height = models.FloatField(null=True,blank=True)
    Height_Unit = models.CharField(max_length=10,default="feet")
    Location_Lat = models.CharField(max_length=20)
    Location_Long = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.Village_Name
    
class TreeMoreDetails(models.Model):
   TempDatabase_id = models.ForeignKey(TempDatabase, on_delete=models.CASCADE, related_name="TempDatabase")
   Girth = models.FloatField()
   Girth_Unit = models.CharField(max_length=10,default="feet")
   Age = models.FloatField()
   Age_Unit = models.CharField(max_length=10,default="Months")
   TreeCanopy = models.FloatField()
   TreeCanopy_Unit = models.CharField(max_length=10,default="Sq. feet")

class PlaceDetails(models.Model):
   District = models.CharField(max_length=20)
   Block = models.CharField(max_length=20)
   GramPanchayat = models.CharField(max_length=50)
   WardNumber = models.CharField(max_length=20)

class TreeLocationsDetails(models.Model):
   TreeData_id = models.ForeignKey(TempDatabase, on_delete=models.CASCADE, related_name="TreeDetails")
   Place_id = models.ForeignKey(PlaceDetails, on_delete=models.CASCADE, related_name="PlaceDetails")

class gov_department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.department_name

class land_ownershipby_gov_ngo(models.Model):
    id = models.AutoField(primary_key=True)
    land_ownership = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.land_ownership

class registration_role_department(models.Model):
    reg_dep_name = models.CharField(max_length=50)

class plantation_bypvt(models.Model):
    plantation_name = models.CharField(max_length=100, null=True, blank=True)
    plantation_height = models.FloatField(null=True, blank=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)

    dict_code = models.ForeignKey(DistrictList, on_delete=models.CASCADE, related_name="pvt_dict" , null=True ,blank=True)
    block_code = models.ForeignKey(BlockList, on_delete=models.CASCADE, related_name="pvt_block" , null=True ,blank=True)
    gp_code = models.ForeignKey(GpFinalList, on_delete=models.CASCADE, related_name="pvt_gp" , null=True ,blank=True)


    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/plant/', unique_filename)

    # Image fields with unique names
    image1 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    # image2 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)

    # submitted_by = models.CharField(max_length=50)
    submitted_by = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="temp_user_for_pvtsubmittedby")
    # this status represent the tree status wheather it is alive or died ..... and if tree is dies then it will represent as True and by default it is false
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id}: Status:{self.status}"
        

class plantation_bygov(models.Model):
    plantation_name = models.CharField(max_length=100, null=True, blank=True)
    plantation_height = models.FloatField(null=True, blank=True)
    gov_department_id = models.ForeignKey(gov_department, on_delete=models.CASCADE, related_name="gov_department_id")
    land_ownership = models.ForeignKey(land_ownershipby_gov_ngo, on_delete=models.CASCADE, related_name="land_ownership_bygov")
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)

    dict_code = models.ForeignKey(DistrictList, on_delete=models.CASCADE, related_name="gov_dict" , null=True ,blank=True)
    block_code = models.ForeignKey(BlockList, on_delete=models.CASCADE, related_name="gov_block" , null=True ,blank=True)
    gp_code = models.ForeignKey(GpFinalList, on_delete=models.CASCADE, related_name="gov_gp" , null=True ,blank=True)


    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/plant/', unique_filename)

    # Image fields with unique names
    image1 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    # image2 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)

    # submitted_by = models.CharField(max_length=50)
    submitted_by = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="temp_user_for_govsubmittedby")
    status = models.BooleanField(null=True, blank=True, default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id}: Status:{self.status}"
        

class plantation_byngo(models.Model):
    plantation_name = models.CharField(max_length=100, null=True, blank=True)
    plantation_height = models.FloatField(null=True, blank=True)
    ngo_name = models.CharField(max_length=100, null=True, blank=True)
    land_ownership = models.ForeignKey(land_ownershipby_gov_ngo, on_delete=models.CASCADE, related_name="land_ownership_byngo")
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)

    dict_code = models.ForeignKey(DistrictList, on_delete=models.CASCADE, related_name="ngo_dict" , null=True ,blank=True)
    block_code = models.ForeignKey(BlockList, on_delete=models.CASCADE, related_name="ngo_block" , null=True ,blank=True)
    gp_code = models.ForeignKey(GpFinalList, on_delete=models.CASCADE, related_name="ngo_gp" , null=True ,blank=True)

    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/plant/', unique_filename)

    # Image fields with unique names
    image1 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    # image2 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=get_unique_image_path, null=True, blank=True)

    # submitted_by = models.CharField(max_length=50)
    submitted_by = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="temp_user_for_ngosubmittedby")
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id}: Status:{self.status}"

class PlantationType(models.Model):
    plantation_type_name = models.CharField(max_length=100, default = False)
    

class Plant(models.Model):
    name = models.CharField(max_length=200, verbose_name="Plant Name")
    synonyms = models.TextField(blank=True, verbose_name="Plant Synonyms")
    hindi_name = models.CharField(max_length=200, blank=True, verbose_name="Plant Hindi Name")
    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/plant/', unique_filename)

    image = models.ImageField(upload_to=get_unique_image_path, blank=True, null=True, verbose_name="Plant Image")

    def __str__(self):
        return self.name



class BlockPlantation(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blockplanatation_submittedby")
    plantation_type = models.ForeignKey(PlantationType, on_delete=models.CASCADE, related_name="blockplanatation_plantatin_type")
    goverment_departmet = models.ForeignKey(gov_department, on_delete=models.CASCADE, related_name="blockplanat_goverment_departmet")
    land_ownership = models.ForeignKey(land_ownershipby_gov_ngo, on_delete=models.CASCADE, related_name = "blockplanat_land_ownership")
    location_list = models.TextField()

    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/blockplantation/', unique_filename)

    image1_block_planation = models.ImageField(upload_to=get_unique_image_path, default="NOT_AVILABE")

    location_lat = models.FloatField()
    location_long = models.FloatField()
    dict_code = models.ForeignKey(DistrictList, on_delete=models.CASCADE, related_name="block_dict" , null=True ,blank=True)
    block_code = models.ForeignKey(BlockList, on_delete=models.CASCADE, related_name="block_block" , null=True ,blank=True)
    gp_code = models.ForeignKey(GpFinalList, on_delete=models.CASCADE, related_name="block_gp" , null=True ,blank=True)
    number_of_plants = models.CharField(max_length=5)
    plantationArea = models.CharField(max_length=3)
    planta_name_text = models.TextField()
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OTP_model(models.Model):
    user_phone = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Set expiration time to current time + 5 minutes
        self.expiration_time = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)


class CertificateStorage(models.Model):
    certificate_id = models.CharField(
        max_length=10,
        primary_key=True,
    )
    # user_id = models.CharField(max_length=10)
    user_id = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name="user_id_certificate")
    certificate_image = models.ImageField(upload_to='images/certificate_image/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.certificate_id


class reward_storage(models.Model):
    plantation_id = models.ForeignKey(plantation_bypvt, on_delete=models.CASCADE, related_name="rewordfor_plantation_bypvt")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plant_Id {self.plantation_id}"





def generate_unique_certificate_id():
    return uuid.uuid4().hex[:10]

class TempStorageCertificateInfo(models.Model):
    user_id = models.CharField(max_length=10)
    certificate_id = models.CharField(
        max_length=10,
        primary_key=True,
        default=generate_unique_certificate_id,
        editable=False,
        unique=True
    )
    plantation_id_bypvt = models.ForeignKey(plantation_bypvt, null=True, blank=True, on_delete=models.CASCADE, related_name="plantation_id_bypvt_provided")
    plantation_id_bygov = models.ForeignKey(plantation_bygov, null=True, blank=True, on_delete=models.CASCADE, related_name="plantation_id_bygov_provided")
    plantation_id_byngo = models.ForeignKey(plantation_byngo, null=True, blank=True, on_delete=models.CASCADE, related_name="plantation_id_byngo_provided")

    def get_unique_image_path(instance, filename):
        ext = filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join('images/selfi/', unique_filename)
    selfi_image = models.ImageField(upload_to=get_unique_image_path)


    certificate_holder_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.certificate_id},{self.user_id}"


# ---------------------------------------------------------- 

from portaldash.models import GpFinalList, BlockList, DistrictList

class GovPlantationAdress(models.Model):
    Plant_id_gov = models.CharField(max_length=100, primary_key=True)
    DISTRICT_C = models.CharField(max_length=100)
    BLOCK_CODE = models.CharField(max_length=100)
    GP_FINAL_C = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Government Plantation Address'
        verbose_name_plural = 'Government Plantation Addresses'

    def __str__(self):
        return f"{self.Plant_id_gov} - {self.DISTRICT_C}"




class PvtPlantationAdress(models.Model):
    Plant_id_pvt = models.CharField(max_length=100, primary_key=True)
    DISTRICT_C = models.CharField(max_length=100)
    BLOCK_CODE = models.CharField(max_length=100)
    GP_FINAL_C = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Private Plantation Address'
        verbose_name_plural = 'Private Plantation Addresses'

    def __str__(self):
        return f"{self.Plant_id_pvt} - {self.DISTRICT_C}"

class NgoPlantationAdress(models.Model):
    Plant_id_ngo = models.CharField(max_length=100, primary_key=True)
    DISTRICT_C = models.CharField(max_length=100)
    BLOCK_CODE = models.CharField(max_length=100)
    GP_FINAL_C = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'NGO Plantation Address'
        verbose_name_plural = 'NGO Plantation Addresses'

    def __str__(self):
        return f"{self.Plant_id_ngo} - {self.DISTRICT_C}"

class BlockPlantationAdress(models.Model):
    BlockPlantation = models.CharField(max_length=100, primary_key=True)
    DISTRICT_C = models.CharField(max_length=100)
    BLOCK_CODE = models.CharField(max_length=100)
    GP_FINAL_C = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Block Plantation Address'
        verbose_name_plural = 'Block Plantation Addresses'

    def __str__(self):
        return f"{self.BlockPlantation} - {self.DISTRICT_C}"
