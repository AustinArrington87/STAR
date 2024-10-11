import pandas as pd
from scipy.stats import pearsonr

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
    summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
    return summary_stats

# Calculate statistics for all fields, corn fields, and soybean fields
all_fields_stats = calculate_summary_stats(data_filtered, 'star_score')
corn_fields = data_filtered[data_filtered['crop_type'] == 'C']
corn_fields_stats = calculate_summary_stats(corn_fields, 'star_score')
soybean_fields = data_filtered[data_filtered['crop_type'] == 'SB']
soybean_fields_stats = calculate_summary_stats(soybean_fields, 'star_score')

# Calculate correlation, R^2, and p-values for each parameter against 'star_score'
means_by_star_score = data_filtered.groupby('star_score').mean().reset_index()
star_scores = means_by_star_score['star_score']

correlation_results = {
    'Parameter': [],
    'Correlation (r)': [],
    'R^2': [],
    'p-value': []
}

for column in columns_of_interest[2:]:  # Skip 'star_score' and 'crop_type'
    param_values = means_by_star_score[column]
    r, p_value = pearsonr(star_scores, param_values)
    correlation_results['Parameter'].append(column)
    correlation_results['Correlation (r)'].append(r)
    correlation_results['R^2'].append(r**2)
    correlation_results['p-value'].append(p_value)

# Convert correlation results to a DataFrame
correlation_df = pd.DataFrame(correlation_results)

# Save all results to an Excel file
output_path = 'star_summary_statistics_with_correlations.xlsx'
with pd.ExcelWriter(output_path) as writer:
    all_fields_stats.to_excel(writer, sheet_name='all_fields', index=False)
    corn_fields_stats.to_excel(writer, sheet_name='corn_fields', index=False)
    soybean_fields_stats.to_excel(writer, sheet_name='soybean_fields', index=False)
    correlation_df.to_excel(writer, sheet_name='correlations', index=False)

print(f"Summary statistics and correlations saved to {output_path}")
