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

# --- INDEX ---
# 1.- Load and cleaning
# 2.- Pivot table
# 3.- KPIs
# 4.- Web aplication


# 1.-----CLEAN DATA--------
df_car_data = car_data
# we need to streamline some data, model_year, cylinders,odometer, is_4w should be int and model
# year and date posted should be changed to datetime fomrat. we have identified 798 files
# with a range of price between 1 and 950 usd, this is not real and will be removing this files
# to have more acuracy as this only represnts 2.65% of data.
# we have encountered that 3531 missing models which represents 7% of missing information.
# we will fill these nan with infomration form the table to minimize infomration lost.
df_car_data_1 = df_car_data.copy()
df_car_data_1[['model_year', 'cylinders', 'odometer', 'is_4wd']] = df_car_data[[
    'model_year', 'cylinders', 'odometer', 'is_4wd']].astype('Int64')
df_car_data_1['model_year'] = pd.to_datetime(
    df_car_data_1['model_year'].astype('Int64'), format='%Y', errors='coerce')
df_car_data_1['date_posted'] = pd.to_datetime(
    df_car_data_1['date_posted'], format='%Y-%m-%d',  errors='coerce')
df_car_data_1 = df_car_data_1[df_car_data_1['price'] > 900]
df_car_data_1['model_year'] = df_car_data_1['model_year'].fillna(
    df_car_data_1.groupby('model')['model_year']
    .transform(lambda s: s.mode().iloc[0])
)

print(df_car_data_1.info())
print('--------------------------------------')
print(df_car_data_1.isnull().sum())
print('--------------------------------------')
print(df_car_data_1.describe())
print('--------------------------------------')
print(df_car_data_1.sample(10))

df_car_data_clean = df_car_data_1.copy()

# 2.---- Pivot tables----
pivot_type_count = pd.pivot_table(
    df_car_data_clean,
    index='type',
    aggfunc='size'
).reset_index(name='count').sort_values('count', ascending=True)


pivot_condition_vs_days = pd.pivot_table(
    df_car_data_clean,
    index='condition',
    values='days_listed',
    aggfunc='mean'
).reset_index()

# ---- UI ----
st.header('Análisis interactivo de vehículos')
# 3.--- KPI ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tipo de Vehiculos", f"{df_car_data_clean['type'].nunique()}")
col2.metric("Inventario Total", f"{len(df_car_data_clean):,}")
col3.metric("Precio Promedio de venta",
            f"{df_car_data_clean['price'].mean():,.2f}")
col4.metric("Dias Promedio para Venta",
            f"{df_car_data_clean['days_listed'].mean():.2f}")


# ---- UI -----
st.markdown(
    """
    Este dashboard fue desarrollado como parte del Proyecto 7 de la cohorte 65 del 
    Bootcamp de Data Analytics de TripleTen. En él, analizamos el comportamiento de venta de un lote 
    de automóviles, explorando patrones, tendencias y factores que influyen en los tiempos de 
    venta y precios.  

    Para su desarrollo se utilizaron herramientas como **Conda**, **Visual Studio Code**, **GitHub** 
    y **Render**, permitiendo integrar el análisis, la visualización y la publicación web de forma 
    eficiente.
    """
)

# 4.-----web aplication -----
# ---- grafics definition ----


def bar_count_by_type():
    "Generates a bar chart that shows the number of vehicles by type"
    bar_fig = px.bar(pivot_type_count,
                     x='type',
                     y='count',
                     )
    bar_text = (
        """
        ### Grafico de Barras
        Nuestro inventario abarca **13 tipos de vehiculos** distintos,
        lo cual refleja una oferta variada pero con un patron claro. 

        la mayor parte del lote se compone de vehículos grandes; SUVs,
        camionetas y pickups.

        En contraste, vehículos que podemos cconsiderar de nicho como, 
        buses, convertibles y off-road, represnetan una pequeña fraccion
        de nuestro lote. 

        Nuestro inventario refleja una clara demanda de vehiculos grandes
        y multifuncionales enfocado a coches de uso familiar o utilitarios.
        """
    )
    return bar_fig, bar_text


def bars_days_by_condition():
    """Generates a horizontal bar chart shows the average number of days a 
    car remains unsold.
    """
    h_bar_fig = px.bar(
        pivot_condition_vs_days,
        x='days_listed',
        y='condition',
        orientation='h',
    )
    h_bar_text = (
        """
        ### Grafico de barras horizontal
        Nuestro analisis revela un proceso de venta estable y consistente, con 
        un promedio de venta de 39 días, sin importar su condicion del vehiculo.

        Esta consistencia  en ventas sugiere un mercado equilibrado en donde
        la oferta y demanda mantienen un ritmo constante y predecible.
        """
    )
    return h_bar_fig, h_bar_text


def heatmap():
    "This heatmap shows the correlation between different variables."
    heatmap_corr = df_car_data_clean[
        ['price', 'model_year', 'odometer', 'days_listed']].corr()
    heatmap_fig = px.imshow(
        heatmap_corr,
        text_auto='.2f',
        zmin=1, zmax=1
    )
    heatmap_text = (
        """
        ### Heatmap
        Al revisar la matriz de correlación de nuestro lote, 
        podemos observar un patorn calro de como el mercado
        pone valor a los vehículos.

        Por un lado tenemos una correlacion positiva entre el modelo
        y el año del vehiculo, entre mas reciente mas costoso; Por el
        otro lado, tenemos una correlacion negativa con el kilometraje,
        entre mas kilometros menos valor del coche. 

        Revisando esta amtriz podemos observar que el mercado fija los
        precios con base en la antiguedad y kilometraje de los vehiculos.
        """
    )
    return heatmap_fig, heatmap_text


def boxplot_price():
    "This chart help us to identify atypical values."
    bplot_fig = px.box(df_car_data_clean, y='price', log_y=True)
    bplot_text = (
        """
        ### Boxplot
        Comenzamos analizando los precios del inventario, que rondan los **12 000 USD**.  
        Sin embargo, al examinar los datos notamos que el rango real de precios oscila entre 
        **5 000 y 17 000 USD**, con una **mediana de 9 500 USD**.  
        Esto indica que la mayoría de los compradores se concentra en el rango de **gama media**.  
        Al observar esta gráfica, podemos concluir que el mercado es **más amplio y diverso** 
        de lo que parece, centrándose principalmente en vehículos de gama media.
        """
    )
    return bplot_fig, bplot_text


def scatter_price_year():
    "Generatres a scatter plot that shows the realtionship between model year and price"
    scatter_fig = px.scatter(
        df_car_data_clean, x='model_year', y='price')
    scatter_text = (
        """
        ### Scatter Plot
        Nuestro inventario abarca desde autos clásicos hasta modelos modernos 
        *(1908–2019)*. La mayoría de los vehículos fueron fabricados entre **2006 y 2014**, 
        con una **media en 2011**.  

        En este rango, los precios oscilan entre **5,500 y 17,000 USD**, 
        lo que refleja un mercado dominado por autos de gama media.

        Los vehículos en los extremos del rango corresponden principalmente a modelos de lujo.  

        A medida que el modelo es más reciente, el precio tiende a aumentar.
        """
    )
    return scatter_fig, scatter_text


def conclusion():
    "Shows final thoughts on this project."
    c_text = (
        """
        Dentro de este proyecto se representa una integración completa de todo lo aprendido durante 
        los primeros siete sprints del programa, en donde realizamos el análisis, la visualización y 
        la implementación de una aplicación web.
        
        Primero se llevó a cabo un proceso de limpieza y homologación de datos, en el cual se 
        eliminaron alrededor del 2.56% de las filas que no presentaban coherencia con el resto del 
        conjunto. Esto nos permitió obtener una vista más real y precisa de la información revisada.  
        
        Para el análisis y la visualización de los datos, utilizamos pivot tables para resumir y 
        facilitar la interpretación de la información. Además, empleamos Plotly y Streamlit para
        generar visualizaciones interactivas, creando cinco tipos de gráficos diferentes que 
        ofrecieron una perspectiva más amplia del conjunto de datos; También elaboramos una matriz 
        de correlación para identificar relaciones relevantes entre distintas variables.  
        
        Adicionalmente, implementamos la herramienta Pylint para limpiar el código, mejorar su 
        estructura y asegurar su legibilidad para cualquier persona que analice el código fuente.  
        
        Finalmente, para el despliegue web, utilizamos los servicios de Render y Streamlit, 
        incorporando botones y filtros interactivos que permiten una exploración dinámica y 
        visualmente atractiva de la información.

        Este proyecto resume de forma práctica los conocimientos adquiridos, integrando técnicas 
        de análisis, visualización y despliegue web en un solo flujo de trabajo.

        Repositorio **GitHub**: https://github.com/AlbertQu1/Sprint_7.git
        """
    )
    return None, c_text


# ---- grafic selection -----
opcion = st.selectbox(
    'Seleccion de grafico',
    ['Distribucion de precios', 'Precio vs Año',
     'Cantidad de vehiculos por tipo', 'Promedio de dias vs Condicion del coche',
     'Heatmap de correlación', 'Conclusión']
)

# Inicializar constantes/modo módulo para evitar uso antes de asignación y cumplir pylint C0103
FIG = None
TEXT = None

if opcion == 'Distribucion de precios':
    FIG, TEXT = boxplot_price()
elif opcion == 'Precio vs Año':
    FIG, TEXT = scatter_price_year()
elif opcion == 'Cantidad de vehiculos por tipo':
    FIG, TEXT = bar_count_by_type()
elif opcion == 'Promedio de dias vs Condicion del coche':
    FIG, TEXT = bars_days_by_condition()
elif opcion == 'Heatmap de correlación':
    FIG, TEXT = heatmap()
elif opcion == 'Conclusión':
    FIG, TEXT = conclusion()

if FIG is not None:
    st.plotly_chart(FIG, use_container_width=True)

if TEXT:
    st.markdown(TEXT)
