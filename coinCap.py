# import libraries
import pandas as pd
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import key
import os
from time import time, sleep
import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px 
import plotly.io as pio

# page configuration
st.set_page_config(
    page_title = 'Cryptocurrency Prices Dashboard',
    page_icon = '✅',
    layout = 'wide'
)


# dashboard title

st.markdown("""
        <h1 style='text-align: center; color: #13DBFB;'>Today's Cryptocurrency Prices</h1>
        """, True)

# about dashboard
st.markdown("""
        <h2 style='text-align: left; color: #FFFFFF;'>Check out the current prices and charts for cryptocurrencies like Bitcoin (BTC), Ethereum (ETH), Tether (USDT), USD Coin (USDC), and BNB (BNB). Market highlights are automatically updated every 60 seconds.</h2>
        """, True)

# creating a single-element container.
placeholder = st.empty()

# data 

column_names = ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'timestamp']
data = [[0, 0, 0, 0, 0, pd.to_datetime('now')]]
df_final = pd.DataFrame(data, columns = column_names)
def api_runner():
    
    global df_final
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'5',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': key.key
    }

    json = requests.get(url, params = parameters, headers = headers ).json()

    coins = pd.json_normalize(json['data'])

    df = coins[['symbol', 'quote.USD.price']]

    df = df.T

    df = df.rename(columns=df.iloc[0]).drop(df.index[0])

    df.reset_index(drop=True, inplace = True)

    df.loc[:,'timestamp'] = pd.to_datetime('now')

    df_final = df_final.append(df)

    
    
#loop

for x in range(60):
    api_runner()
    
    btc = df_final['BTC'].iloc[-1]
    eth = df_final['ETH'].iloc[-1]
    usdt = df_final['USDT'].iloc[-1]
    usdc = df_final['USDC'].iloc[-1]
    bnb = df_final['BNB'].iloc[-1]
    
    btc2 = df_final['BTC'].iloc[-2]
    eth2 = df_final['ETH'].iloc[-2]
    usdt2 = df_final['USDT'].iloc[-2]
    usdc2 = df_final['USDC'].iloc[-2]
    bnb2 = df_final['BNB'].iloc[-2]

    with placeholder.container():
        with open('style.css') as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        # create three columns
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="BTC", value= f"$ {round(btc,2)}", delta= round((btc-btc2),2))
        kpi2.metric(label="ETH", value= f"$ {round(eth,2)}", delta= round((eth-eth2),2))
        kpi3.metric(label="USDT", value= f"$ {round(usdt,4)}", delta= round((usdt-usdt2),4))
        kpi4.metric(label="USDC", value= f"$ {round(usdc,2)}", delta= round((usdc-usdc2),2))
        kpi5.metric(label="BNB", value= f"$ {round(bnb,2)}", delta= round((bnb-bnb2),2))
        
        st.markdown("""
        <br/>
        """, True)
        # create two columns for charts 
      
        st.markdown("""
        <h2 style='text-align: Center; color: #13DBFB;'>Trend every 60 seconds.</h2>
        """, True)

        fig_col1, fig_col2, fig_col3, fig_col4, fig_col5 = st.columns(5)
        with fig_col1:
            fig1 = px.line(data_frame = df_final.iloc[1:], x = 'timestamp', y = 'BTC', template = 'plotly_dark',
                         color_discrete_sequence = px.colors.qualitative.T10, title = "BTC Trend by Minutes")
            st.write(fig1)
        with fig_col2:
            fig2 = px.line(data_frame = df_final.iloc[1:], x = 'timestamp', y = 'ETH', template = 'plotly_dark',
                         color_discrete_sequence = px.colors.qualitative.T10, title = "ETH Trend by Minutes")
            st.write(fig2)
        with fig_col3:
            fig3 = px.line(data_frame = df_final.iloc[1:], x = 'timestamp', y = 'USDT', template = 'plotly_dark',
                         color_discrete_sequence = px.colors.qualitative.T10, title = "USDT Trend by Minutes")
            st.write(fig3)
        with fig_col4:
            fig4 = px.line(data_frame = df_final.iloc[1:], x = 'timestamp', y = 'USDC', template = 'plotly_dark',
                         color_discrete_sequence = px.colors.qualitative.T10, title = "USDC Trend by Minutes")
            st.write(fig4)
        with fig_col5:
            fig5 = px.line(data_frame = df_final.iloc[1:], x = 'timestamp', y = 'BNB', template = 'plotly_dark',
                         color_discrete_sequence = px.colors.qualitative.T10, title = "BNB Trend by Minutes")
            st.write(fig5)
        
        st.markdown("""
        <br/>
        """, True)
        
        #table
        st.markdown("""
        <h2 style='text-align: Center; color: #13DBFB;'>Examine the data more closely.</h2>
        """, True)
        df_final.reset_index(drop=True, inplace = True)
        st.table(df_final.iloc[1:])
    
    sleep(60)
