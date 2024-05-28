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

plt.title('Moisture over Time', fontsize=20, pad=20)  # Set the title with additional spacing
plt.grid(True)  # Show grid

# Set y-axis limits
plt.ylim(35, 95)

# Set x-axis ticks
plt.xticks(plt.xticks()[0], [f'Day {i+1}' for i in range(len(plt.xticks()[0]))], fontsize=13)

# Add '%' to y-axis ticks
plt.gca().set_yticklabels([f'{int(x)}%' for x in plt.gca().get_yticks()], fontsize=13)

plt.legend(fontsize=16)  # Show legend

# Adjust layout
plt.tight_layout(pad=2)  # Add even spacing around the graph
plt.subplots_adjust(top=0.9)  # Add spacing around the title

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'combined_plots.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots saved to: {output_filename}')
