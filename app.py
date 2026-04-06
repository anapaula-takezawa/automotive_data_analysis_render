import pandas as pd
import plotly.express as px
import streamlit as st

st.header('🚗 Análise de Veículos Usados')

car_data = pd.read_csv('vehicles.csv')

# checkbox histograma
build_hist = st.checkbox('Mostrar histograma')

if build_hist:
    st.write('Histograma da quilometragem')
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, width='stretch')

# checkbox scatter
build_scatter = st.checkbox('Mostrar gráfico de dispersão')

if build_scatter:
    st.write('Quilometragem vs Preço')
    fig = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig, width='stretch')