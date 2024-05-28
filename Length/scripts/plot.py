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
plt.plot(first_df.index + 1, first_df['length'], label=label_mapping.get(first_file, first_file.split(".")[0]))  # Plot data

# Iterate through the remaining files and plot their datasets on the same axes
for file in files[1:]:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Plot 'time' vs. 'length' on the same axes
    plt.plot(df.index + 1, df['length'], label=label_mapping.get(file, file.split(".")[0]))  # Plot data

plt.title('Growth over Time', fontsize=20, y=1.05)  # Set the title with font size and adjusted spacing
plt.grid(True)  # Show grid

plt.legend(fontsize=16)  # Show legend with font size

plt.xticks(range(1, len(first_df) + 1, 4), [f'Day {i}' for i in range(1, len(first_df) + 1, 4)], fontsize=13)

# Format y-axis with "cm" after each value and remove decimal point if integer
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x) if x.is_integer() else x:.0f} cm'))

# Set font size for y-axis ticks
plt.yticks(fontsize=13)

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'combined_plots.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots saved to: {output_filename}')
