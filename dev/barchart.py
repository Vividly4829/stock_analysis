import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px


def load_and_aggregate_holdings(directory, currency: str):
    # List all JSON files in the directory
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
        
        holdings_data = []

        # Process each file
        for file_name in json_files:
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                date = file_name.split('.')[0]  # Assuming the file name is the date
                for holding in data['holdings']:
                    holding['Date'] = date
                    holdings_data.append(holding)

        # Convert to DataFrame
        df = pd.DataFrame(holdings_data)

        currency_columns = [f'Value ({currency})']

        # Aggregate data
        category_totals_per_day = df.groupby(['Date', 'Category'])[
            'Value (NOK)'].sum().reset_index()
        
        return category_totals_per_day
    
barchart_data = load_and_aggregate_holdings(f'data/ruben/portfolioLogs/MonaOne', 'NOK')

print(barchart_data)

# Plotting
# fig, ax = plt.subplots()
# barchart_data.plot(kind='bar', stacked=True, ax=ax)

# # Customizing the plot
# ax.set_title("Total Value of Holdings per Category per Day")
# ax.set_xlabel("Date")
# ax.set_ylabel("Total Value (NOK)")
# plt.xticks(rotation=45)
# plt.show()


# fig = px.bar(barchart_data, x="Date", y=[
#              "gold", "silver", "bronze"], title="Wide-Form Input")
# fig.show()


fig = px.bar(barchart_data, x='Date', y='Value (NOK)', color='Category',
             title="Total Value of Holdings per Category per Day",
             labels={'Value (NOK)': 'Total Value (NOK)'},  color_discrete_sequence=px.colors.qualitative.G10)

# Display the plot
fig.show()
