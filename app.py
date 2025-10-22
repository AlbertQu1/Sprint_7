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

# ---- pivot tables used for grafics ----
pivot_type_count = pd.pivot_table(
    df_car_data_clean,
    index='type',
    values='price',
    aggfunc='count'
).reset_index()

pivot_condition_vs_days = pd.pivot_table(
    df_car_data_clean,
    index='condition',
    values='days_listed',
    aggfunc='mean'
).reset_index()

pivot_heatmap = pd.pivot_table(
    df_car_data_clean,
    index='condition',
    columns='type',
    values='days_listed',
    aggfunc='mean'
).reset_index()

# -----web aplication -----
# ---- UI -----
st.header('Análisis interactivo de vehículos')
st.markdown("""
Estamos trabajando el sprint 7, de la cohorte 65.
""")

# ---- grafics definition ----


def bar_count_by_type():
    fig = px.bar(pivot_type_count,
                 x='type',
                 y='price',
                 )
    text = (
        '**test 3***'
    )
    return fig, text


def bars_days_by_condition():
    fig = px.bar(
        pivot_condition_vs_days,
        x='days_listed',
        y='condition',
        orientation='h',
        title='PENDIENTE'
    )
    text = (
        'test 4'
    )
    return fig, text


def heatmap():
    fig = px.imshow(
        pivot_heatmap
    )
    text = (
        'test 5'
    )
    return fig, text


def boxplot_price():
    fig = px.box(df_car_data_clean, y='price',
                 title='Distribuicion de precio de vehiculos')
    text = (
        '**test 1**'
    )
    return fig, text


def scatter_price_year():
    fig = px.scatter(
        df_car_data_clean, x='model_year', y='price', trendline='ols')
    text = (
        '**test 2**'
    )
    return fig, text


# ---- grafic selection -----
opcion = st.selectbox(
    'Seleccion de grafico',
    ['Distribucion de precios', 'Precio vs Año',
        'Cantidad de vehiculos por tipo', 'Promedio de dias vs Condicion del coche', 'Heatmap tiempo de venta']
)

if opcion == 'Distribucion de precios':
    fig, text = boxplot_price()
elif opcion == 'Precio vs Año':
    fig, text = scatter_price_year()
elif opcion == 'Cantidad de vehiculos por tipo':
    fig, text = bar_count_by_type()
elif opcion == 'Promedio de dias vs Condicion del coche':
    fig, text = bars_days_by_condition()
elif opcion == 'Heatmap tiempo de venta':
    fig, text = heatmap()

st.plotly_chart(fig, use_container_width=True)
st.markdown(text)
