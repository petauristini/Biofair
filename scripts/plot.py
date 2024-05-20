import pandas as pd
import matplotlib.pyplot as plt
import os

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'cleaned_data')
files = os.listdir(data_dir)

# Read the first CSV file into a DataFrame to initialize the plot
first_df = pd.read_csv(os.path.join(data_dir, files[0]))

# Convert 'time' column to datetime format
first_df['time'] = pd.to_datetime(first_df['time'])

plt.style.use('dark_background')

# Create the plot with the first dataset
plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(first_df['time'], first_df['moisture'], label=files[0].split(".")[0])  # Plot data

# Iterate through the remaining files and plot their datasets on the same axes
for file in files[1:]:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Plot 'time' vs. 'moisture' on the same axes
    plt.plot(df['time'], df['moisture'], label=file.split(".")[0])  # Plot data

# Add labels and title
plt.xlabel('Time')  # Set the x-axis label
plt.ylabel('Moisture')  # Set the y-axis label
plt.title('Moisture over Time')  # Set the title
plt.grid(True)  # Show grid
plt.legend()  # Show legend

# Adjust layout
plt.tight_layout()

# Save the plot as an image file
output_filename = os.path.join(parent_dir, 'plots', 'combined_plots.png')
plt.savefig(output_filename)
print(f'Combined plots saved to: {output_filename}')
