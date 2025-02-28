import pandas as pd
import numpy as np

# Load the Excel file
file_path = "Producer Field Export.xlsx"  
try:
    xls = pd.ExcelFile(file_path)
    print("Excel file loaded successfully.")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()

# Load the "Field Forms" sheet
df_field_forms = pd.read_excel(xls, sheet_name="Field Forms")
print(f"Loaded 'Field Forms' sheet with {len(df_field_forms)} rows.")

# Function to determine the sample size
def calculate_sample_size(n):
    return int(np.ceil(np.sqrt(n)))

# Filter only submitted forms (excluding in-progress)
df_submitted = df_field_forms.dropna(subset=["Submitted At"])
print(f"Filtered submitted forms: {len(df_submitted)} rows.")

if df_submitted.empty:
    print("No submitted forms found. Exiting.")
    exit()

# Group by crop year to determine sample size per year
sampled_dfs = []
extra_samples = 10  # Extra fields in case of refusals/unreachable producers

for year, group in df_submitted.groupby("Year"):
    total_submissions = len(group)
    sample_size = calculate_sample_size(total_submissions)
    print(f"Year {year}: Total {total_submissions} submissions, selecting {sample_size}.")

    # Random sampling
    sampled = group.sample(n=min(sample_size, total_submissions), random_state=42)
    
    # Ensuring each field form type (e.g., grasses, grains, legumes) is included
    field_form_types = group["Form Name"].unique()
    for form in field_form_types:
        if form not in sampled["Form Name"].values:
            additional = group[group["Form Name"] == form].sample(n=1, random_state=42)
            sampled = pd.concat([sampled, additional])
    
    # Adding extra randomly selected fields
    extra_sampled = group.drop(sampled.index, errors='ignore').sample(n=min(extra_samples, len(group) - len(sampled)), random_state=42)
    sampled = pd.concat([sampled, extra_sampled])
    
    print(f"Year {year}: Selected {len(sampled)} fields.")
    
    # Append results
    sampled_dfs.append(sampled)

# Concatenating all sampled data
if sampled_dfs:
    df_sampled = pd.concat(sampled_dfs)
    output_path = "Sampled_Field_Forms.xlsx"
    df_sampled.to_excel(output_path, index=False)
    print(f"Sampled field forms saved to: {output_path}")
else:
    print("No sampled data was generated.")
