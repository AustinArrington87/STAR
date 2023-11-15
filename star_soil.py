import pandas as pd
import numpy as np

# header names for reference 
#Address, Current Crop Abbreviation, Winter hardy single species, Winter hardy multiple species
#Winter kill single species, Winter kill multiple species, Cover crop terminated after cash crop planting
#Fall no till or low disturbance fert bar, Fall strip till on non-HEL, Fall shank and no other tillage, 
#Fall full width not exceeding 3 inch depth, Fall full width exceeding 3 inch depth, Fall full width on soybean stubble
#Spring no till or low disturbance fert bar, Spring strip till or freshener on non-HEL OR Spring shank and no other spring tillage, 
#Spring full width single pass and no fall tillage, Spring full width two or more passes and no fall tillage, Spring full width one or more passes and fall tillage


def create_subsample(input_csv, output_csv):
    # Load the CSV file
    d = pd.read_csv(input_csv)

    data = d[1:]  # Excluding the header row

    # Column letters to indices (considering that pandas index starts from 0)
    columns_indices = {
        'F': 5, 'P': 15, 'AO': 40, 'AP': 41, 'AQ': 42, 'AR': 43, 'AS': 44,
        'AY': 50, 'AZ': 51, 'BA': 52, 'BB': 53, 'BC': 54, 'BD': 55,
        'BE': 56, 'BF': 57, 'BG': 58, 'BH': 59, 'BI': 60
    }

    # Extracting the required columns
    selected_columns = [data.columns[i] for i in columns_indices.values()]

    # Create a subsample of 50 random rows based on the specified columns
    random_indices = np.random.choice(data.index, size=50, replace=False)
    random_sample = data.iloc[random_indices]

    # Save the subsample (with all columns) to a new CSV file
    random_sample.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Define the input and output file paths
    input_csv = 'STAR_2022.csv'  # Replace with your input CSV file path
    output_csv = 'STAR_2022_updated.csv'  # Replace with your desired output CSV file path

    # Create the subsample and save to the output file
    create_subsample(input_csv, output_csv)
