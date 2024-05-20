import os
import pandas as pd

# Get the parent directory path of the current script file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Create a directory named 'formatted_data' in the parent directory to store the results if it doesn't exist
output_dir = os.path.join(parent_dir, 'formatted_data')
os.makedirs(output_dir, exist_ok=True)

# Path to the history.csv file located in the parent directory
csv_file_path = os.path.join(parent_dir, 'history.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Create an empty DataFrame to store lines that could not be processed
dump_df = pd.DataFrame(columns=df.columns)

# Extract the unique plant identifiers from the original 'entity_id' column
df['entity_id'] = df['entity_id'].str.extract(r'sensor\.plantesp_plants_(\d+)_moisture')
df['entity_id'] = 'plants_' + df['entity_id']

# Identify rows with missing plant identifiers
missing_plant_id = df['entity_id'].isna()

# Write rows with missing plant identifiers to a dump file
dump_df = df[missing_plant_id]
dump_df.to_csv(os.path.join(output_dir, 'dump.csv'), index=False)
print(f'Saved lines with missing plant identifiers to "{os.path.join(output_dir, "dump.csv")}"')

# Drop rows with missing plant identifiers from the main DataFrame
df = df.dropna(subset=['entity_id'])

# Loop through each unique plant and create a separate CSV file
for plant in df['entity_id'].unique():
    # Filter the DataFrame for the current plant
    plant_df = df[df['entity_id'] == plant].copy()  # Use copy to avoid SettingWithCopyWarning

    # Rename the 'state' column to 'moisture'
    plant_df.rename(columns={'state': 'moisture'}, inplace=True)

    # Convert 'last_changed' column to datetime format
    plant_df['time'] = pd.to_datetime(plant_df['last_changed'])

    # Sort the DataFrame by the 'time' column
    plant_df.sort_values(by='time', inplace=True)

    # Drop the 'entity_id' and 'last_changed' columns
    plant_df = plant_df.drop(columns=['entity_id', 'last_changed'])

    # Reorder the columns to have 'time' first and then 'moisture'
    plant_df = plant_df[['time', 'moisture']]

    # Format 'time' column as desired
    plant_df['time'] = plant_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Example format: YYYY-MM-DD HH:MM:SS

    # Write the filtered DataFrame to a new CSV file in the output directory
    output_filename = os.path.join(output_dir, f'{plant}.csv')
    plant_df.to_csv(output_filename, index=False)
    print(f'Created file: {output_filename}')
