import pandas as pd
import numpy as np
import os

# Load the Excel file
file_path = "Producer Field Export.xlsx" 
xls = pd.ExcelFile(file_path)

# Load required sheets
df_field_forms = pd.read_excel(xls, sheet_name="Field Forms")
df_producers = pd.read_excel(xls, sheet_name="Producers")

# Function to determine the sample size
def calculate_sample_size(n):
    return int(np.ceil(np.sqrt(n)))

# Filter only submitted forms (excluding in-progress)
df_submitted = df_field_forms.dropna(subset=["Submitted At"])

if df_submitted.empty:
    print("No submitted field forms found. Exiting.")
    exit()

# Select relevant columns from Producers sheet
producer_cols = ["User ID", "First Name", "Last Name", "Address", "City", "State", "Zip", "County", "Phone"]
df_producers_selected = df_producers[producer_cols]

# Group by crop year to determine sample size per year
sampled_dfs = []
extra_samples = 10  # Extra fields for refusals/unreachable producers

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
    print(f"Total sampled records: {len(df_sampled)}")

    # Merge with producer details
    df_sampled_with_producers = df_sampled.merge(df_producers_selected, on="User ID", how="left")
    print(f"Merged with producer details: {len(df_sampled_with_producers)} records")

    # Set output file path
    output_path = os.path.expanduser("Sampled_Field_Forms.xlsx")

    try:
        df_sampled_with_producers.to_excel(output_path, index=False)
        print(f"✅ Sampled field forms saved successfully to: {output_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
else:
    print("No sampled data was generated.")
