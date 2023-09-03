import pandas as pd 
import streamlit as st

@st.cache_data

def find_proxy_etf(age_years):
# open the files/etf_list/most_traded_etfs_with_annualised_return.xlsx file
    df = pd.read_excel('files\\etf_list\\most_traded_etfs_with_annualised_return.xlsx')
    # Remove all the ETFs from the df that have an inception date after the cuurent year minus the variable age_years
    df = df[df['Inception Date'] < pd.Timestamp(pd.Timestamp.now().year - age_years, 1, 1)]
    return df


