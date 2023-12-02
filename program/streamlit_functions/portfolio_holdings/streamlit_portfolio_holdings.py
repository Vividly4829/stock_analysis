from program.workers.portfolio_parser import *
import streamlit as st
import plotly.express as px
import pandas as pd

st.write('Current holdings')

def streamlit_portfolio_holdings():
    trigger_rerun = False

    if st.sidebar.button('Load current valuation of portfolio'):
        st.session_state.loaded_portfolio.holdings = calculate_portfolio_value(st.session_state.loaded_portfolio.holdings)
        trigger_rerun = True

    if 'loaded_portfolio' in st.session_state:

        df = pd.DataFrame(st.session_state.loaded_portfolio.holdings)
        
        # Multi-select for accounts and categories
        available_accounts = df['Account'].unique().tolist()
        selected_accounts = st.multiselect('Select Accounts', available_accounts, default=available_accounts)
        df = df[df['Account'].isin(selected_accounts)]
        
        available_categories = df['Category'].unique().tolist()
        selected_categories = st.multiselect('Select Categories', available_categories, default=available_categories)
        df = df[df['Category'].isin(selected_categories)]

        # Currency selection
        currency_options = ['NOK', 'USD', 'EUR']
        selected_currency = st.selectbox('Choose Currency', currency_options)
        
        total_value = df[f'Value ({selected_currency})'].sum()

        # Sunburst Layer Selection
        with st.form('Sunburst Layers Form'):
            options = ['Account', 'Category', 'Ticker']
            first_layer = st.selectbox('Select the inner circle', options)
            second_options = [opt for opt in options if opt != first_layer]
            second_layer = st.selectbox('Select the second circle', second_options)
            submit_button = st.form_submit_button('Update Sunburst Chart')
            
            if submit_button:
                fig_sunburst = px.sunburst(df, path=[first_layer, second_layer], values=f'Value ({selected_currency})', title=f'Sunburst Chart (Total: {total_value:,.2f} {selected_currency})')

                # Custom hover template to show both value and percentage of total
                hover_template = "%{label}<br>Value: %{value:,.2f}<br>Percentage: %{percent:.1%}"
                fig_sunburst.update_traces(hovertemplate=hover_template)
                
                fig_sunburst.update_layout(height=1200, width=1200)
                st.plotly_chart(fig_sunburst)
            
        # Show the filtered dataframe
        st.dataframe(df, width=1000, height=1000)

    else:
        st.info('No portfolio loaded - load portfolio in side menu.')

    if trigger_rerun:
        st.experimental_rerun()