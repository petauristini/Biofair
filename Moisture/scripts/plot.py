import pandas as pd
import matplotlib.pyplot as plt
import os

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'averaged_data')
files = ['plants_1.csv', 'plants_2.csv', 'plants_3.csv', 'plants_4.csv']

output_dir = os.path.join(parent_dir, 'plots')
os.makedirs(output_dir, exist_ok=True)

# Mapping from filenames to labels
label_mapping = {
    'plants_1.csv': 'Group 1: high frequency, high power',
    'plants_2.csv': 'Group 2: high frequency, low power',
    'plants_3.csv': 'Group 3: low frequency, high power',
    'plants_4.csv': 'Control Group'
}

# Read the first CSV file into a DataFrame to initialize the plot
first_file = files[0]
first_df = pd.read_csv(os.path.join(data_dir, first_file))

# Convert 'time' column to datetime format
first_df['time'] = pd.to_datetime(first_df['time'])

# Create the plot with the first dataset
plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(first_df['time'], first_df['moisture'], label=label_mapping.get(first_file, first_file.split(".")[0]))  # Plot data

# Iterate through the remaining files and plot their datasets on the same axes
for file in files[1:]:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Plot 'time' vs. 'moisture' on the same axes
    plt.plot(df['time'], df['moisture'], label=label_mapping.get(file, file.split(".")[0]))  # Plot data

# Add labels and title
plt.xlabel('Time')  # Set the x-axis label
plt.ylabel('Moisture')  # Set the y-axis label
plt.title('Moisture over Time')  # Set the title
plt.grid(True)  # Show grid

# Set y-axis limits
plt.ylim(35, 95)

plt.legend()  # Show legend

# Adjust layout
plt.tight_layout()

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'combined_plots.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots saved to: {output_filename}')
