import streamlit as st
import plotly.express as px
import pandas as pd


def streamlit_portfolio_holdings():
    st.session_state['trigger_rerun'] = False


    if 'loaded_portfolio' not in st.session_state:
        st.info('No portfolio loaded - load portfolio in side menu.')
        return None

    dataframe_tab, sunburst_tab = st.tabs(["Dataframe", "Sunburst"])


    df = st.session_state.loaded_portfolio.holdings
    
    # Multi-select for accounts and categories
    available_accounts = df['Account'].unique().tolist()
    selected_accounts = dataframe_tab.multiselect('Select Accounts', available_accounts, default=available_accounts)
    df = df[df['Account'].isin(selected_accounts)]
    
    available_categories = df['Category'].unique().tolist()
    selected_categories = dataframe_tab.multiselect(
        'Select Categories', available_categories, default=available_categories)
    df = df[df['Category'].isin(selected_categories)]

    # Currency selection
    currency_options = ['NOK', 'USD', 'EUR']
    selected_currency = dataframe_tab.selectbox('Choose Currency', currency_options)
    
    total_value = df[f'Value ({selected_currency})'].sum()
    dataframe_tab.header(f'Total portfolio value: {total_value:,.2f} {selected_currency}')

    # Sunburst Layer Selection

    options = ['Account', 'Category', 'Ticker']
    first_layer = sunburst_tab.selectbox('Select the inner circle', options)
    second_options = [opt for opt in options if opt != first_layer]
    second_layer = sunburst_tab.selectbox('Select the second circle', second_options)
    


    fig_sunburst = px.sunburst(df, path=[first_layer, second_layer], values=f'Value ({selected_currency})', title=f'Sunburst Chart (Total: {total_value:,.2f} {selected_currency})')

    # Custom hover template to show both value and percentage of total
    hover_template = "%{label}<br>Value: %{value:,.2f}<br>Percentage: %{percent:.1%}"
    fig_sunburst.update_traces(hovertemplate=hover_template)
    
    fig_sunburst.update_layout(height=1200, width=1200)
    sunburst_tab.plotly_chart(fig_sunburst)
        
    # Show the filtered dataframe

    # add a heatmap styling to the dataframe
    df = df.style.background_gradient(cmap='Reds', subset=[f'Value ({selected_currency})'])
    dataframe_tab.dataframe(df, width=1000, height=700)


    if st.session_state['trigger_rerun']:
        st.experimental_rerun()