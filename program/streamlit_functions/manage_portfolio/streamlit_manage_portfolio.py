import streamlit as st
from program.streamlit_functions.manage_portfolio.log_change import log_portfolio_change    
from program.workers.jsonbase import *
import pandas as pd

def streamlit_manage_portfolio():


    st.session_state['trigger_rerun'] = False
    
    if not 'loaded_portfolio' in st.session_state:
        st.info('No portfolio loaded - load portfolio in side menu.')
  
    if 'loaded_portfolio' in st.session_state:
        st.sidebar.write('Options:')
        if st.sidebar.button('Load inception dates:'):
            with st.spinner('Loading inception dates...'):
                st.session_state['trigger_rerun'] = True
                st.session_state.loaded_portfolio.load_inception_dates()
   
        df = pd.DataFrame(st.session_state.loaded_portfolio.holdings)
    
        # Multi-select for accounts and categories
        available_accounts = df['Account'].unique().tolist()
        selected_accounts = st.multiselect('Select Accounts', available_accounts, default=available_accounts)
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
        st.markdown('---')
    
        log_portfolio_change(df)

        st.markdown('---')

        df = df.style.background_gradient(cmap='Reds', subset=[f'Value ({selected_currency})'])
        st.dataframe(df, width=1000)


        with st.expander("Manage types"):
      
            # Create a streamlit select box to select a types
            if st.session_state.loaded_portfolio.types is not None:
                types = st.selectbox(
                    "Select types", options=list(st.session_state.loaded_portfolio.types))
                if st.button('Delete types'):
                    st.session_state.loaded_portfolio.types.remove(types)
                    st.session_state.loaded_portfolio.update_portfolio_types()
                    st.success(f'types {types} deleted')
                    st.session_state['trigger_rerun'] = True

                
                new_type = st.text_input("Add new types")
                if st.button('Add types'):
                    st.session_state.loaded_portfolio.types.append(new_type)
                    st.session_state.loaded_portfolio.update_portfolio_types()
                    st.success(f'types {new_type} added')
                    st.session_state['trigger_rerun'] = True

            
        with st.expander("Manage accounts"):
            # Create a streamlit select box to select an account
            if st.session_state.loaded_portfolio.accounts is not None:
                account = st.selectbox(
                    "Select account", options=list(st.session_state.loaded_portfolio.accounts))
                if st.button('Delete account'):
                    st.session_state.loaded_portfolio.accounts.remove(account)
                    st.session_state.loaded_portfolio.update_portfolio_accounts()
                    st.success(f'Account {account} deleted')
                    st.session_state['trigger_rerun'] = True

                new_account = st.text_input("Add new account")
                if st.button('Add account'):
                    if new_account is not None:
                        if len(new_account) > 0 and new_account not in st.session_state.loaded_portfolio.accounts:
                            st.session_state.loaded_portfolio.accounts.append(new_account)
                            st.session_state.loaded_portfolio.update_portfolio_accounts()
                            st.success(f'Account {new_account} added')
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error(f'Account {new_account} was not added.')

        with st.expander("Manage categories"):
            # Create a streamlit select box to select an account
            if st.session_state.loaded_portfolio.categories is not None:
                category = st.selectbox(
                    "Select category", options=list(st.session_state.loaded_portfolio.categories))
                if st.button('Delete category'):
                    st.session_state.loaded_portfolio.categories.remove(category)
                    st.session_state.loaded_portfolio.update_portfolio_categories()
                    st.success(f'Category {category} deleted')
                    st.session_state['trigger_rerun'] = True

                new_category = st.text_input("Add new category")
                if st.button('Add category'):
                    if new_category is not None:
                        if len(new_category) > 1 and new_category not in st.session_state.loaded_portfolio.categories:
                            st.session_state.loaded_portfolio.categories.append(new_category)
                            st.session_state.loaded_portfolio.update_portfolio_categories()
                            st.success(f'Category {new_category} added')
                            
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error(f'Category {new_category} was not added because it was too short or already existed.')
               

        with st.expander("Upload portfolio from excel"):
            # Create a streamlit form to upload a portfolio from an excel file
           
            with open("files\\portfolios\\formue.xlsx", "rb") as file:

                st.download_button(
                    label="Download excel template",
                    data=file,
                    file_name="excel_portfolio_template.xlsx",
                    mime="application/wps-office.xlsx/xlsx"
                )

            with st.form(key="Upload portfolio"):
                excel_file = st.file_uploader(
                    "Upload excel file", type=['xlsx'])

                if st.form_submit_button(label="Upload portfolio"):
                    if excel_file is not None:
                        df = pd.read_excel(excel_file)
                        df_dict = df.to_dict(orient='records')

                        upload_status = st.session_state.loaded_portfolio.upload_excel_portfolio(df_dict)

                        if upload_status:
                            st.success("Portfolio uploaded")
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error("Failed to upload portfolio")
                    else:
                        st.error("No excel file uploaded")

    
        if 'trigger_rerun' in st.session_state:
   
            if st.session_state.trigger_rerun:

                if 'rerun_count' not in st.session_state:
                    st.session_state.rerun_count = 1
                else:
                    st.session_state.rerun_count += 1
                print(
                    f'reran program for the {st.session_state.rerun_count} time')
                st.experimental_rerun()
