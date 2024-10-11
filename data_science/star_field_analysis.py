import pandas as pd

# Developed by Austin Arrington, PLANT Group LLC

# Load the dataset
file_path = 'star_field_outcomes_flat.csv'
data = pd.read_csv(file_path)

# Define the relevant columns for analysis
columns_of_interest = [
    'star_score', 'crop_type',
    'CC_nlrs3_nitrate_EQ5', 'CC_nlrs3_phosphorus_EQ6', 'CC_nlrs4_sediment_EQ9', 
    'CC_nrls4_CO2e', 'RT_nrls5_phosphorus_EQ6', 'RT_nrls5_sediment_EQ10', 
    'RT_nrls5_CO2e', 'MRTN_nlrs1_nitrate_EQ8', 'PRATE_nlrs07_phosphorus_EQ7'
]

# Filter the data to include only the relevant columns
data_filtered = data[columns_of_interest]

# Function to calculate summary statistics for each star score within the dataset
def calculate_summary_stats(data, group_by_column):
    summary_stats = data.groupby(group_by_column).agg(['mean', 'min', 'max', 'std']).reset_index()
    # Flatten column headers for Excel compatibility
    summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
    return summary_stats

# Calculate statistics for all fields
all_fields_stats = calculate_summary_stats(data_filtered, 'star_score')

# Filter data for corn fields and calculate statistics
corn_fields = data_filtered[data_filtered['crop_type'] == 'C']
corn_fields_stats = calculate_summary_stats(corn_fields, 'star_score')

# Filter data for soybean fields and calculate statistics
soybean_fields = data_filtered[data_filtered['crop_type'] == 'SB']
soybean_fields_stats = calculate_summary_stats(soybean_fields, 'star_score')

# Save the results to an Excel file with each table in a separate sheet
output_path = 'star_summary_statistics_AA.xlsx'
with pd.ExcelWriter(output_path) as writer:
    all_fields_stats.to_excel(writer, sheet_name='all_fields', index=False)
    corn_fields_stats.to_excel(writer, sheet_name='corn_fields', index=False)
    soybean_fields_stats.to_excel(writer, sheet_name='soybean_fields', index=False)

print(f"Summary statistics saved to {output_path}")
