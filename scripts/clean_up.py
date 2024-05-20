import pandas as pd
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'formatted_data')
files = os.listdir(data_dir)
files.remove('dump.csv')

output_dir = os.path.join(parent_dir, 'cleaned_data')
os.makedirs(output_dir, exist_ok=True)

for file in files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Convert 'moisture' column to numeric
    df['moisture'] = pd.to_numeric(df['moisture'], errors='coerce')

    # Drop rows with NaN values in 'moisture' column
    df.dropna(subset=['moisture'], inplace=True)

    # Set 'time' column as the index
    df.set_index('time', inplace=True)

    # Resample the DataFrame to hourly frequency and calculate the mean
    hourly_avg_df = df.resample('1H').mean()

    # Reset index to make 'time' a column again
    hourly_avg_df.reset_index(inplace=True)

    output_filename = os.path.join(output_dir, file)
    hourly_avg_df.to_csv(output_filename, index=False)
    print(f'Created file: {output_filename}')
