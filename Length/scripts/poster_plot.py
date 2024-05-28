import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter

# Define parent and data directories
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'raw_data')
files = ['plants_1.csv', 'plants_2.csv', 'plants_3.csv', 'plants_4.csv']

output_dir = os.path.join(parent_dir, 'plots')
os.makedirs(output_dir, exist_ok=True)

# Mapping from filenames to labels and colors
label_mapping = {
    'plants_1.csv': ('Group 1:\nhigh frequency, high power', 'blue'),
    'plants_2.csv': ('Group 2:\nhigh frequency, low power', 'orange'),
    'plants_3.csv': ('Group 3:\nlow frequency, high power', 'green'),
    'plants_4.csv': ('Control Group', 'red')
}

# Function to format y-axis labels with 'cm'
def cm_formatter(x, pos):
    return f'{int(x)} cm'

# Set up a single figure to contain all subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Standart Deviation', fontsize=24)

# Iterate through the files and plot their datasets with mean and standard deviation
for idx, file in enumerate(files):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))
    
    # Rename columns for easier access
    df.columns = ['time', 'List 1', 'List 2', 'List 3', 'List 4']

    # Convert 'time' column to datetime format
    df['time'] = pd.to_datetime(df['time'], format='%d.%m.%y')

    # Calculate the number of days since the first date
    df['days'] = (df['time'] - df['time'].min()).dt.days + 1

    # Calculate mean and standard deviation across the lists for each time point
    df['mean'] = df[['List 1', 'List 2', 'List 3', 'List 4']].mean(axis=1)
    df['std'] = df[['List 1', 'List 2', 'List 3', 'List 4']].std(axis=1)

    # Plot the mean and standard deviation
    row = idx // 2
    col = idx % 2
    axs[row, col].plot(df['days'], df['mean'], label=label_mapping[file][0], color=label_mapping[file][1])
    axs[row, col].fill_between(df['days'], df['mean'] - df['std'], df['mean'] + df['std'], alpha=0.2, color=label_mapping[file][1])

    # Set labels and legend for each subplot with increased font size
    axs[row, col].legend(loc='upper left', fontsize=17)  # Increase legend text size here
    axs[row, col].grid(True)

    # Set x-ticks to every 4 days and create corresponding labels
    xticks = df['days'][::4]
    xtick_labels = [f'Day {day}' for day in xticks]
    axs[row, col].set_xticks(xticks)
    axs[row, col].set_xticklabels(xtick_labels, fontsize=13)  # Increase font size of x-tick labels

    # Apply y-axis formatter to add 'cm' after each value
    axs[row, col].yaxis.set_major_formatter(FuncFormatter(cm_formatter))

    # Increase font size of tick values on both axes
    axs[row, col].tick_params(axis='both', which='major', labelsize=14)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the plot as an image file
output_filename = os.path.join(output_dir, 'poster_plot.png')
plt.savefig(output_filename, dpi=300)
print(f'Combined plots with standard deviation saved to: {output_filename}')
