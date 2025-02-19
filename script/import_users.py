import csv
import os
import uuid
from datetime import datetime
from account.models import User  # Replace 'your_app' with the actual app name
from api.models import BlockPlantation, PlantationType, gov_department, land_ownershipby_gov_ngo
from portaldash.models import GpFinalList, BlockList, DistrictList

def parse_datetime(date_str):
    """Helper function to parse datetime strings."""
    if date_str and date_str != 'NULL':
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))  # Handle 'Z' as UTC
        except ValueError:
            return None
    return None

def get_unique_image_path(instance, filename):
    """Generate unique file path for the image."""
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/blockplantation/', unique_filename)

# Specify the path to your CSV file
csv_path = 'script/BLOCK_PLANTATION.csv'  # Replace with the actual path to your CSV file

# Open the CSV file with utf-8 encoding to handle special characters
with open(csv_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ['status']  # Add new column to mark new plantations
    rows = []
    plantations = []

    for row in reader:
        plantation_area_value = row['plantationArea']
        plantation_area_value = str(plantation_area_value)[:3]
        
        # Fetch the related fields
        submitted_by = User.objects.filter(id=int(row['submitted_by_id'])).first() if row.get('submitted_by_id') else None
        plantation_type = PlantationType.objects.filter(id=int(row['plantation_type_id'])).first() if row.get('plantation_type_id') else None
        goverment_departmet = gov_department.objects.filter(id=int(row['goverment_departmet_id'])).first() if row.get('goverment_departmet_id') else None
        land_ownership = land_ownershipby_gov_ngo.objects.filter(id=int(row['land_ownership_id'])).first() if row.get('land_ownership_id') else None
        dict_code = DistrictList.objects.filter(DISTRICT_C=row['dict_code_id']).first() if row.get('dict_code_id') else None
        block_code = BlockList.objects.filter(BLOCK_C=row['block_code_id']).first() if row.get('block_code_id') else None
        gp_code = GpFinalList.objects.filter(GP_FINAL_C=row['gp_code_id']).first() if row.get('gp_code_id') else None

        if not gp_code:
            gp_code=None
            print(f"gp_code with ID {row['gp_code_id']} not found in the database.")
        if not block_code:
            print(f"block_code with ID {row['block_code_id']} not found in the database.")
            block_code=None
        if not dict_code:
            print(f"dict_code_id with ID {row['dict_code_id']} not found in the database.")
            dict_code=None
        # If the user is not found, print the row's user ID
        if not submitted_by:
            print(f"User with ID {row['submitted_by_id']} not found in the database.")
        else:
            # Create the BlockPlantation instance
            plantation = BlockPlantation(
                id=row['id'],
                submitted_by=submitted_by,
                plantation_type=plantation_type,
                goverment_departmet=goverment_departmet,
                land_ownership=land_ownership,
                location_list=row['location_list'],
                image1_block_planation=row.get('image1_block_planation', 'NOT_AVILABE'),  # Set a default image path if necessary
                location_lat=float(row['location_lat']) if row.get('location_lat') else None,
                location_long=float(row['location_long']) if row.get('location_long') else None,
                dict_code=dict_code,
                block_code=block_code,
                gp_code=gp_code,
                number_of_plants=row['number_of_plants'],
                plantationArea=plantation_area_value,
                planta_name_text=row['planta_name_text'],
                status=False,
                created_at=parse_datetime(row['created_at']),
                updated_at=parse_datetime(row['updated_at']),
            )
        
            # Add new plantation to list
            plantations.append(plantation)
            row['status'] = 'New'  # Mark as 'New' if it's a new plantation

            rows.append(row)

# Bulk insert the remaining new plantations
BlockPlantation.objects.bulk_create(plantations)
print("Block plantations have been successfully imported.")

# Save the updated rows (with 'status' column to indicate new plantations) back to the CSV
