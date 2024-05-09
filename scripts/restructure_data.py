import pandas as pd
import os

data_folder = 'scripts/data'
output_folder = 'scripts/data'

# Function to extract the parent project ID
def extract_parent_id(project_number):
    # Find the first occurrence of either '-' or '.'
    first_dash = project_number.find('-')
    first_period = project_number.find('.')
    
    # Determine the earliest valid separator position
    if first_dash == -1 and first_period == -1:
        return project_number  # No separator found, return the whole number
    elif first_dash == -1:
        return project_number[:first_period]
    elif first_period == -1:
        return project_number[:first_dash]
    else:
        return project_number[:min(first_dash, first_period)]

for filename in os.listdir(data_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_folder, filename)
        data = pd.read_csv(file_path)

        # Apply the function to create a new column
        data['parent_project_id'] = data['Project Number Ref'].apply(extract_parent_id)

        # Save the modified data to a new CSV file in the same folder
        output_path = os.path.join(output_folder, filename)
        data.to_csv(output_path, index=False)

        print(f"Processed {filename} and saved to {output_path}.")

print("Data processing complete. 'Parent Project ID' added and saved to 'updated_projects.csv'.")