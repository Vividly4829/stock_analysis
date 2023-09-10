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
         # Show the dataframe
        # st.dataframe(df, width=2000, height=1000)

        total_value = df['Value (NOK)'].sum()

        try:
               # Generate the charts with actual values and total value
            # Generate the pie charts with actual values and total value
            for title, chart_df, x, y in [
                ('Distribution Per Account', df, 'Account', 'Value (NOK)'),
                ('Distribution Per Category', df, 'Category', 'Value (NOK)')
            ]:
                fig = px.pie(chart_df, names=x, values=y, title=f"{title} (Total: {total_value:,} NOK)")
                fig.update_traces(textinfo='percent+label+value')
                fig.update_layout(height=400, width=600)
                st.plotly_chart(fig)
            
            # Sunburst Chart with Category in the middle, extending to individual assets
            fig_sunburst = px.sunburst(df, path=['Category', 'Account', 'Ticker'], values='Value (NOK)', title=f'Sunburst Chart for Category, Account, and Ticker (Total: {total_value:,} NOK)')
            
            # Custom hover template to show both value and percentage of total
            hover_template = "%{label}<br>Value: %{value:,}<br>Percentage: %{percent:.1%}"
            fig_sunburst.update_traces(hovertemplate=hover_template)
            
            fig_sunburst.update_layout(height=12000, width=1200)
            st.plotly_chart(fig_sunburst)


            if trigger_rerun:
                st.experimental_rerun()
        except:
            st.error('Failed to generate charts, remember to load valuations first.')

   
        
        # Show the dataframe
        st.dataframe(df, width=1000, height=1000)

    else:
        st.info('No portfolio loaded - load portfolio in side menu.')

    if trigger_rerun:
        st.experimental_rerun()
