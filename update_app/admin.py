from django.contrib import admin
from django.apps import apps
from django.contrib.admin.filters import SimpleListFilter

from .models import PlantHealthStatus, CenterIndividualPlantation_99, UpdateData_99

class PlantHealthStatusFilter(SimpleListFilter):
    title = 'Health Status'
    parameter_name = 'health_status'

    def lookups(self, request, model_admin):
        return [(status.id, status.health_status_en) for status in PlantHealthStatus.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(current_health_status__id=self.value())
        return queryset

class CenterIndividualPlantation_99Filter(SimpleListFilter):
    title = 'Plantation ID'
    parameter_name = 'plantation_id'

    def lookups(self, request, model_admin):
        return [(plantation.PLantid, plantation.PLantid) for plantation in CenterIndividualPlantation_99.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(center_entry_plant__PLantid=self.value())
        return queryset

class UpdateData_99Admin(admin.ModelAdmin):
    list_filter = [PlantHealthStatusFilter, CenterIndividualPlantation_99Filter]

admin.site.register(PlantHealthStatus)
admin.site.register(CenterIndividualPlantation_99)
admin.site.register(UpdateData_99, UpdateData_99Admin)
