"""
Average the data from all plants in one group and save it to a new CSV file.
"""

import pandas as pd
import os

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'raw_data')
files = os.listdir(data_dir)

output_dir = os.path.join(parent_dir, 'averaged_data')
os.makedirs(output_dir, exist_ok=True)

for file in files:
    df = pd.read_csv(os.path.join(data_dir, file))

    # Convert the 'Index' column to datetime format (adjust the format as needed)
    df['time'] = pd.to_datetime(df['Index'], format='%d.%m.%y')

    # Compute the average of List 1 to List 4
    df['length'] = df[['List 1', 'List 2', 'List 3', 'List 4']].mean(axis=1)

    # Select the relevant columns (Index and Average)
    result_df = df[['time', 'length']]

    # Save the resulting DataFrame to a new CSV file
    output_filename = os.path.join(output_dir, file)
    result_df.to_csv(output_filename, index=False)
    print(f'Averaged data saved to: {output_filename}')
