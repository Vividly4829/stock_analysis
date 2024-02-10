import streamlit as st
import plotly.express as px
import plotly.express as px
from program.workers.aggregate_holdings_over_time import load_and_aggregate_holdings
import plotly.graph_objects as go
from program.streamlit_functions.portfolio_holdings.back_test.back_test import back_test


def streamlit_portfolio_holdings():
    st.session_state['trigger_rerun'] = False

    if 'loaded_portfolio' not in st.session_state:
        st.info('No portfolio loaded - load portfolio in side menu.')
        return None

    df = st.session_state.loaded_portfolio.holdings

    # Multi-select for accounts and categories
    available_accounts = df['Account'].unique().tolist()
    selected_accounts = st.multiselect(
        'Select Accounts', available_accounts, default=available_accounts)
    df = df[df['Account'].isin(selected_accounts)]

    available_categories = df['Category'].unique().tolist()
    selected_categories = st.multiselect(
        'Select Categories', available_categories, default=available_categories)
    df = df[df['Category'].isin(selected_categories)]

    # Currency selection
    currency_options = ['NOK', 'USD', 'EUR']
    selected_currency = st.selectbox('Choose Currency', currency_options)

    total_value = df[f'Value ({selected_currency})'].sum()
    st.header(f'Total portfolio value: {total_value:,.2f} {selected_currency}')

    dataframe_tab, sunburst_tab, historical_performance, backtest = st.tabs(
        ["Dataframe", "Sunburst", "Historical performance", "backtest"])

    ################ SUNBURST TAB ################

    options = ['Category', 'Ticker', 'Account']
    first_layer = sunburst_tab.selectbox(
        'Select the inner circle', options, index=0)
    second_options = [opt for opt in options if opt != first_layer]
    second_layer = sunburst_tab.selectbox(
        'Select the second circle', second_options, index=0)
    third_options = [opt for opt in options if opt !=
                     first_layer and opt != second_layer]
    third_layer = sunburst_tab.selectbox(
        'Select the third circle', third_options, index=0)

    fig_sunburst = px.sunburst(df, path=[first_layer, second_layer, third_layer],
                               values=f'Value ({selected_currency})', title=f'Sunburst Chart (Total: {total_value:,.2f} {selected_currency})')

    # Update the traces to show label and percentage on the chart
    fig_sunburst.update_traces(textinfo='label+percent parent')

    fig_sunburst.update_layout(height=1200, width=1200)
    sunburst_tab.plotly_chart(fig_sunburst)

    ################ DATAFRAME TAB ################

    # Add a heatmap styling to the dataframe
    df = df.style.background_gradient(
        cmap='Reds', subset=[f'Value ({selected_currency})'])
    dataframe_tab.dataframe(df, width=1000, height=700)

    if st.session_state['trigger_rerun']:
        st.experimental_rerun()

    ################# STACKED BAR CHART #################

    category_totals_per_day = load_and_aggregate_holdings(
        f'data/{st.session_state.loaded_portfolio.user_name}/portfolioLogs/{st.session_state.loaded_portfolio.user_portfolio_name}', selected_currency)

    fig = go.Figure()

    # Get unique categories and dates
    categories = category_totals_per_day['Category'].unique()
    dates = category_totals_per_day['Date'].unique()

    # Adding each category as a separate trace
    for category in categories:
        filtered_data = category_totals_per_day[category_totals_per_day['Category'] == category]
        fig.add_trace(go.Bar(
            x=filtered_data['Date'],
            y=filtered_data['Value (NOK)'],
            # Show percentage with 2 decimal places
            text=filtered_data['Percentage'].apply(lambda x: f'{x:.2f}%'),
            textposition='inside',
            name=category
        ))

    # Update the layout for a stacked bar chart
    fig.update_layout(
        barmode='stack',
        title="Total Value of Holdings per Category per Day",
        xaxis_title="Date",
        yaxis_title="Total Value (NOK)",
        height=1000
    )

    historical_performance.plotly_chart(fig, use_container_width=True)

    # Pivot the data to wide format
    wide_format_data = category_totals_per_day.pivot(
        index='Date', columns='Category', values='Value (NOK)').fillna(0)

    # Reset index to make 'Date' a column
    wide_format_data.reset_index(inplace=True)

    # Create a new figure
    fig = go.Figure()

    # Add each category as a separate trace
    for category in wide_format_data.columns[1:]:  # Skip the 'Date' column
        fig.add_trace(go.Scatter(
            x=wide_format_data['Date'],
            # Cumulative sum for stacked area plot
            y=wide_format_data[category],
            mode='lines',
            name=category,
            stackgroup='one'  # Define stack group
        ))

    # Show the plot
    historical_performance.plotly_chart(fig, use_container_width=True)

    # Backtest tab
    back_test()
