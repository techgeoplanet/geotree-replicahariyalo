from rest_framework import serializers
from django.apps import apps

def get_dynamic_serializer(model_name):
    """Dynamically generate a serializer for the given model name."""
    # Fetch model dynamically
    Model = apps.get_model('update_app', model_name)
    if not Model:
        raise LookupError(f"Model {model_name} does not exist.")

    # Create a serializer class dynamically
    class DynamicSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Model
            fields = [
                'PLantid',
                'owner_name',
                'plant_name',
                'height',
                'latitude',
                'longitude',
                'address_gp_id',
                'land_ownership',
                'imageurl_1',
                'imageurl_2',
                'submitted_by_user_id',
                'submitted_by_department_id',
                'submitted_by_ngo_name',
                'status',
                'plant_alive_status',
                'any_update_status',
                'created_at',
                'updated_at',
            ]

    return DynamicSerializer

def get_dynamic_update_data_serializer(model_name):
    """Dynamically generate a serializer for the given model name."""
    # Fetch model dynamically
    Model = apps.get_model('update_app', model_name)
    if not Model:
        raise LookupError(f"Model {model_name} does not exist.")

    # Create a serializer class dynamically
    class DynamicSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Model
            fields = [
                'user',
                'center_entry_plant',
                'health_status',
                'Update_image1',
                'height_infeet',
                'girth_infeet',
                'canopy_infeet',
                'status_date_mmyyyy',
                'status_time',
            ]

    return DynamicSerializer



