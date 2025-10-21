import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv(
    r'https://raw.githubusercontent.com/AlbertQu1/Sprint_7/refs/heads/main/vehicles_us.csv')

st.header('Car Data')  # titulo
