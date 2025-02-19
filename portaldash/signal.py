from django.db.models import F
from .models import ShortDatabase_normal

def update_short_table(GP_FINAL_C, update_field, increment_value=1):
    # print(GP_FINAL_C, update_field, increment_value)
    increment_value = int(increment_value)
    # Perform the increment operation
    queryset = ShortDatabase_normal.objects.filter(GP_FINAL_C=GP_FINAL_C)
    
    # Ensure the field exists
    if hasattr(ShortDatabase_normal, update_field):
        queryset.update(**{update_field: F(update_field) + increment_value})
    else:
        raise ValueError(f"Field {update_field} does not exist in the model.")



# Example usage
# update_short_table(GP_FINAL_C="0808", update_field='Total_Tag_Tree_Verify_C', increment_value=10)
