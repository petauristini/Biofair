import pandas as pd
import matplotlib.pyplot as plt
import os

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'raw_data')
files = ['plants_1.csv', 'plants_2.csv', 'plants_3.csv', 'plants_4.csv']

output_dir = os.path.join(parent_dir, 'plots')
os.makedirs(output_dir, exist_ok=True)

# Mapping from filenames to labels and colors
label_mapping = {
    'plants_1.csv': ('Group 1: high frequency, high power', 'blue'),
    'plants_2.csv': ('Group 2: high frequency, low power', 'orange'),
    'plants_3.csv': ('Group 3: low frequency, high power', 'green'),
    'plants_4.csv': ('Control Group', 'red')
}

# Set up a single figure to contain all subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Growth over Time', fontsize=16)

# Iterate through the files and plot their datasets with mean and standard deviation
for idx, file in enumerate(files):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))
    
    # Rename columns for easier access
    df.columns = ['time', 'List 1', 'List 2', 'List 3', 'List 4']

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%y')

    # Calculate mean and standard deviation across the lists for each time point
    df['mean'] = df[['List 1', 'List 2', 'List 3', 'List 4']].mean(axis=1)
    df['std'] = df[['List 1', 'List 2', 'List 3', 'List 4']].std(axis=1)

    # Plot the mean and standard deviation
    row = idx // 2
    col = idx % 2
    axs[row, col].plot(df['time'], df['mean'], label=label_mapping[file][0], color=label_mapping[file][1])
    axs[row, col].fill_between(df['time'], df['mean'] - df['std'], df['mean'] + df['std'], alpha=0.2, color=label_mapping[file][1])

    # Set labels and legend for each subplot
    axs[row, col].set_xlabel('Time (days)')
    axs[row, col].set_ylabel('Length (cm)')
    axs[row, col].legend(loc='upper left')
    axs[row, col].grid(True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'combined_plots_with_std.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots with standard deviation saved to: {output_filename}')
