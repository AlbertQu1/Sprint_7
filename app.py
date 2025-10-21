'''
Sprint 7
'''
import pandas as pd
import plotly.express as px
import streamlit as st

# file loaded raw github
car_data = pd.read_csv(
    r'https://raw.githubusercontent.com/AlbertQu1/Sprint_7/refs/heads/main/vehicles_us.csv')

# ----UI----
st.header('Sprint 7. Cohorte 35')

st.markdown("""
Estamos trabajando apra hacer el rpyecto del sprint 7.
""")

# -----CLEAN DATA--------
df_car_data = car_data
# print(df_car_data.info())
# we need to streamline some data, model_year, cylinders,odometer, is_4w should be int and model
# year and date posted should be changed to datetime fomrat.
df_car_data_1 = df_car_data.copy()
df_car_data_1[['model_year', 'cylinders', 'odometer', 'is_4wd']] = df_car_data[[
    'model_year', 'cylinders', 'odometer', 'is_4wd']].astype('Int64')
df_car_data_1['model_year'] = pd.to_datetime(
    df_car_data_1['model_year'].astype('Int64'), format='%Y', errors='coerce')
df_car_data_1['date_posted'] = pd.to_datetime(
    df_car_data_1['date_posted'], format='%Y-%m-%d',  errors='coerce')

print(df_car_data_1.info())
print('--------------------------------------')
print(df_car_data_1.isnull().sum())
print('--------------------------------------')
print(df_car_data_1.sample(10))

df_car_data_clean = df_car_data_1.copy()
