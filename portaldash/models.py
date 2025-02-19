from django.db import models
from django.utils import timezone
from datetime import timedelta


class ShortDatabase_normal (models.Model):
    DISTRICT_C = models.CharField(max_length=15)
    DISTRICT_N = models.CharField(max_length=35)

    BLOCK_C = models.CharField(max_length=15)
    BLOCK_N = models.CharField(max_length=35)

    GP_FINAL_C = models.CharField(max_length=15)
    GP_FINAL_N = models.CharField(max_length=35)

    Total_Tag_Tree_Verify_C = models.IntegerField(null=True, blank=True)
    Total_Tag_Tree_Non_Verify_C = models.IntegerField(null=True, blank=True)

    Total_block_plantation_Verify_C = models.IntegerField(null=True, blank=True)
    Total_block_plantation_Non_Verify_C = models.IntegerField(null=True, blank=True)



class ShortDatabase_chart(models.Model):
    unique_id_code = models.CharField(max_length=35)
    value = models.FloatField()  # Assuming value is a float, change it if necessary
    date = models.DateField()

    def __str__(self):
        return f"{self.unique_id_code} - {self.date}"

class ShortDatabase_deTable(models.Model):
    unique_id_code = models.CharField(max_length=35)
    department_name = models.CharField(max_length=100)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.unique_id_code} - {self.department_name} - {self.date}"

        



class DistrictList(models.Model):
    DISTRICT_C = models.CharField(max_length=10, primary_key=True)
    DISTRICT_N = models.CharField(max_length=35)

    def __str__(self):
        return self.DISTRICT_N

class BlockList(models.Model):
    BLOCK_C = models.CharField(max_length=10, primary_key=True)
    BLOCK_N = models.CharField(max_length=35)

    def __str__(self):
        return self.BLOCK_N

class GpFinalList(models.Model):
    GP_FINAL_C = models.CharField(max_length=15, primary_key=True)
    GP_FINAL_N = models.CharField(max_length=50)

    def __str__(self):
        return self.GP_FINAL_N




class SiteVisitCount(models.Model):
    SiteVisitCount = models.IntegerField()

class TotalNumberOfPlantations(models.Model):
    TotalPlantations = models.IntegerField()