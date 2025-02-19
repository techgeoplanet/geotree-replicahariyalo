import pandas as pd
from api_nursery.models import Block, District, GramPanchayat

def transferdata():
    # Specify the CSV file path
    csv_file = 'api_nursery/df_gp.csv'  # Ensure this path is correct

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        skipped_rows = 0  # Track skipped rows

        # Iterate through the DataFrame and add data to the GramPanchayat model
        for _, row in df.iterrows():
            # Check if the corresponding District instance exists
            district_instance = District.objects.filter(District_id=row['DISTRICT_C']).first()
            block_instance = Block.objects.filter(block_id=row['BLOCK_CODE']).first()

            # If the District or Block doesn't exist, skip the row and print a message
            if not district_instance:
                print(f"District with code {row['DISTRICT_C']} does not exist. Skipping row.")
                skipped_rows += 1
                continue  # Skip to next row if District is not found

            if not block_instance:
                print(f"Block with code {row['BLOCK_CODE']} does not exist. Skipping row.")
                skipped_rows += 1
                continue  # Skip to next row if Block is not found

            # Create a GramPanchayat entry if both District and Block exist
            GramPanchayat.objects.create(
                gp_id=row['GP_FINAL_C'],
                gp_name=row['GP_FINAL'],  # Ensure this matches your model field
                block=block_instance,
                District=district_instance  # Assign the District instance
            )

        # Print the number of skipped rows and success message
        print(f"Total skipped rows: {skipped_rows}")
        print("Data successfully added to the GramPanchayat model.")
    
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
