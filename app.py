'''
Sprint 7
'''
import pandas as pd
import plotly.express as px
import streamlit as st

# file loaded raw github
car_data = pd.read_csv(
    r'https://raw.githubusercontent.com/AlbertQu1/Sprint_7/refs/heads/main/vehicles_us.csv'
)

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

# print(df_car_data_1.info())
# print('--------------------------------------')
# print(df_car_data_1.isnull().sum())
# print('--------------------------------------')
# print(df_car_data_1.sample(10))
df_car_data_clean = df_car_data_1.copy()

# -----web aplication -----
# ---- UI -----
st.header('Análisis interactivo de vehículos')
st.markdown("""
Estamos trabajando el sprint 7, de la cohorte 65.
""")

# ---- grafics definition ----


def boxplot_price():
    fig_box = px.box(df_car_data_clean, y='price',
                     title='Distribuicion de precio de vehiculos')
    explanation_1 = (
        '**test**'
    )
    return fig_box, explanation_1


def scatter_price_year():
    fig_scatter = px.scatter(
        df_car_data_clean, x='model_year', y='price', trendline='ols')
    explanation_2 = (
        '**test**'
    )
    return fig_scatter, explanation_2


# ---- grafic selection -----
opcion = st.selectbox(
    'Seleccion de grafico',
    ['Distribucion de precios', 'Precio vs Año']
)

if opcion == 'Distribucion de precios':
    fig, text = boxplot_price()
elif opcion == 'Precio vs Año':
    fig, text = scatter_price_year()
