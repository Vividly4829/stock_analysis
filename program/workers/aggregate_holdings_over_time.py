import os
import pandas as pd
import json
import matplotlib.pyplot as plt


def load_and_aggregate_holdings(directory, currency):
    # List all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    selected_currency = f'Value ({currency})'
    holdings_data = []

    # Process each file
    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Assuming the file name is the date
            date = file_name.split('.')[0]
            for holding in data['holdings']:
                holding['Date'] = date
                holdings_data.append(holding)

    # Convert to DataFrame
    df = pd.DataFrame(holdings_data)

    # Aggregate data by Date and Category, summing up the selected_currency
    category_totals_per_day = df.groupby(['Date', 'Category'])[
        selected_currency].sum().reset_index()

    # Calculate the total value per day
    total_per_day = category_totals_per_day.groupby(
        'Date')[selected_currency].sum().reset_index(name='Total Value')

    # Merge to get total per day for each row
    category_totals_per_day = category_totals_per_day.merge(
        total_per_day, on='Date')

    # Calculate the percentage of each category
    category_totals_per_day['Percentage'] = (
        category_totals_per_day[selected_currency] / category_totals_per_day['Total Value']) * 100

    return category_totals_per_day


