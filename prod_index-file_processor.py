import csv
import json
from datetime import datetime
import sys
import os
# import pandas as pd

def parse_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d-%b-%y %H:%M:%S")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
                except ValueError:
                    return date_str
    return date_obj.strftime("%d-%b-%y")

# Check if a file was dragged onto the script
if len(sys.argv) > 1:
    # The first command-line argument is the path to the dragged file
    file_path = sys.argv[1]
    
    # Extract the date from the filename
    file_name = os.path.basename(file_path)
    date_str = file_name.split(".")[2]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d-%b-%y")
    filename_date = date_obj.strftime("%d%m%Y")
    
    # Set the CSV filename
    csv_filename = f"DSB_Proprietary-Index-Enumerations_Website-Publication_{filename_date}.csv"
    # Set the XLSX filename
    # xlsx_filename = f"DSB_Proprietary-Index-Enumerations_Website-Publication_{filename_date}.xlsx"
    
    # Read the JSON data from the file
    with open(file_path, "r") as file:
        json_data = file.read()
    
        # Parse the JSON data
        data = json.loads(json_data)
    
        # Extract the desired fields from each result and apply formatting/conversion
        results = data["results"]
        formatted_data = []
        for result in results:
            date_str = result["content"]["ISIN"]["LastUpdateDateTime"]
            asset_class = result["content"]["Header"]["AssetClass"]
            index_name = result["content"]["Attributes"]["IndexName"]
            constituent_totv = result["content"]["Attributes"]["ConstituentuTOTV"]
    
            # Parse and format the date
            formatted_date = parse_date(date_str)
            # formatted_date = get_first_word(date_str)
    
            # Convert 'TRUE' to 'YES' and 'FALSE' to 'NO'
            converted_constituent_totv = "YES" if constituent_totv == "TRUE" else "NO"
    
            formatted_data.append([formatted_date, asset_class, index_name, converted_constituent_totv])
    
    
        # Add the headers to the formatted data
        # Sort the formatted data by the third column (index 2)
        sorted_data = sorted(formatted_data, key=lambda x: x[2])
    
        sorted_data.insert(0, ["LastUpdateDateTime", "AssetClass", "IndexName", "ConstituentuTOTV"])
        # Write the sorted data to the CSV file
        with open(csv_filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(sorted_data)
    
        print(f"Data has been written to {csv_filename}.")
        
        # Convert CSV to XLSX
        # df = pd.read_csv(csv_filename)
        # df.to_excel(xlsx_filename, index=False)
        # print(f"Data has been converted to {xlsx_filename}.")
                # Convert CSV to XLSX
    
else:
    print(f"Data has been written to {csv_filename}.")
