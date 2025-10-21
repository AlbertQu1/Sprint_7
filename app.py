import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv(
    r'C:\Users\alber\OneDrive\Documentos\GitHub\Sprint_7\vehicles_us.csv')

st.header('Car Data')  # titulo
