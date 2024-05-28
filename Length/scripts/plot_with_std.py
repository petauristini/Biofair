import pandas as pd
import matplotlib.pyplot as plt
import os

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'raw_data')
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

plt.figure(figsize=(10, 6))  # Set the figure size

# Iterate through the files and plot their datasets with mean and standard deviation
for file in files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))
    
    # Rename columns for easier access
    df.columns = ['time', 'List 1', 'List 2', 'List 3', 'List 4']

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%y')

    # Calculate mean and standard deviation across the lists for each time point
    df['mean'] = df[['List 1', 'List 2', 'List 3', 'List 4']].mean(axis=1)
    df['std'] = df[['List 1', 'List 2', 'List 3', 'List 4']].std(axis=1)

    # Plot the mean
    plt.plot(df['time'], df['mean'], label=label_mapping.get(file, file.split(".")[0]))

    # Plot the standard deviation as a shaded area
    plt.fill_between(df['time'], df['mean'] - df['std'], df['mean'] + df['std'], alpha=0.2)

# Add labels and title with units
plt.xlabel('Time (days)')  # Set the x-axis label with units
plt.ylabel('Length (cm)')  # Set the y-axis label with units
plt.title('Growth over Time')  # Set the title
plt.grid(True)  # Show grid

plt.legend(loc='upper left')  # Show legend on the top left

# Adjust layout
plt.tight_layout()

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'combined_plots_with_std.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots with standard deviation saved to: {output_filename}')
