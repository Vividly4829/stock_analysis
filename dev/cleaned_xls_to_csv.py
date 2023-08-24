import pandas as pd
import os 
# Print current working directory

# Path to the XLS file
xls_file_path = 'dev\\P6000203005.xls'

# Path to save the cleaned XLS data as a CSV file
cleaned_xls_csv_path = 'cleaned_xls_data.csv'
# Reading the content of the XLS file as text
with open(xls_file_path, 'r', encoding='latin1') as file:
    html_content = file.read()

# Parsing the HTML content to extract tables
xls_html_data = pd.read_html(html_content)
first_table = xls_html_data[0]

# Extract the header information and set it as the column names
header_row = first_table.iloc[0]
first_table.columns = header_row

# Remove the header row from the data
first_table = first_table.drop(0)

# Replace non-breaking spaces with regular spaces
first_table = first_table.applymap(lambda x: str(x).replace('\\xa0', ' '))

# Remove the empty row at the beginning of the cleaned XLS data
first_table = first_table.dropna(how='all')

# Save the cleaned XLS data as a CSV file
first_table.to_csv(cleaned_xls_csv_path, index=False)

print('Parse success!')