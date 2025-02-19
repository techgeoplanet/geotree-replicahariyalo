from django.db import models
from django.utils import timezone
from django.conf import settings
from api.models import gov_department

class District(models.Model):
    District_id = models.IntegerField(unique=True, primary_key=True)
    District_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.District_name


class Block(models.Model):
    block_id = models.IntegerField(unique=True, primary_key=True)
    District = models.ForeignKey(District, on_delete=models.CASCADE, related_name='blocks')
    block_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.block_name} ({self.District.District_name})"


class GramPanchayat(models.Model):
    gp_id = models.IntegerField(unique=True, primary_key=True)
    District = models.ForeignKey(District, on_delete=models.CASCADE, related_name='gps')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='gps')
    gp_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gp_name} ({self.block.block_name}, {self.District.District_name})"


class Plant_List(models.Model):
    Plant_id = models.IntegerField(unique=True, primary_key=True)
    Specis = models.CharField(max_length=255)
    Plant_Name = models.CharField(max_length=255)
    Plant_Name_hindi = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Plant_Name} ({self.Specis})"


class NurseryDetails(models.Model):
    LOCATION_FILLING_CHOICES = [
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    OWNERSHIP_CHOICES = [
        ('private', '1'),
        ('government', '2'),
    ]
    nursery_id = models.AutoField(primary_key=True)
    nursery_name = models.CharField(max_length=255, blank=True, null=True)
    depart_id = models.ForeignKey(gov_department, on_delete=models.CASCADE, related_name='nurseries')
    ownership = models.CharField(max_length=10, choices=OWNERSHIP_CHOICES, default='government')
    image_nursery = models.ImageField(upload_to='nursery_images/')
    total_quantity_of_plants = models.IntegerField()
    total_type_of_plants = models.IntegerField()
    asfs_no = models.CharField(max_length=255, blank=True, null=True)
    khasra_no = models.CharField(max_length=255, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    location_filling = models.CharField(max_length=6, choices=LOCATION_FILLING_CHOICES, default='auto')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    gram_panchayat = models.ForeignKey(GramPanchayat, on_delete=models.CASCADE, related_name='nurseries')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='nurseries')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Nursery {self.nursery_id} - {self.gram_panchayat.gp_name}"


class ListOfPlantsInNursery(models.Model):
    NurseryId = models.ForeignKey(NurseryDetails, on_delete=models.CASCADE, related_name='plant_list')
    plant_id = models.ForeignKey(Plant_List, on_delete=models.CASCADE, related_name='nurseries')
    NameOfPlant = models.CharField(max_length=255)
    quantity_of_plants = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.NameOfPlant} - {self.quantity_of_plants} plants"
