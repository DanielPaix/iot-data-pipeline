import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# conexão com banco
engine = create_engine('postgresql://postgres:1234@localhost:5432/iot_db')

# função para carregar dados
def load_data(query):
    return pd.read_sql(query, engine)

# =========================
# TÍTULO
# =========================
st.title('📊 Dashboard de Temperaturas IoT')
st.markdown("### Análise de Dados de Sensores IoT")
st.write("Monitoramento interativo de temperatura com dados de dispositivos IoT.")

# =========================
# DADOS
# =========================
df_avg = load_data("SELECT * FROM avg_temp_por_room")
df_hora = load_data("SELECT * FROM leituras_por_hora")
df_temp = load_data("SELECT * FROM temp_max_min_por_dia")

# =========================
# FILTRO INTERATIVO
# =========================
room_filter = st.selectbox(
    "Selecione o ambiente:",
    df_avg['room_id'].unique()
)

df_filtered = df_avg[df_avg['room_id'] == room_filter]

# =========================
# KPI (DESTAQUE)
# =========================
st.subheader("📌 Indicadores Gerais")

col1, col2, col3 = st.columns(3)

col1.metric("Temp Média", f"{df_avg['avg_temp'].mean():.2f} °C")
col2.metric("Temp Máxima", f"{df_temp['temp_max'].max():.2f} °C")
col3.metric("Temp Mínima", f"{df_temp['temp_min'].min():.2f} °C")

st.markdown("---")

# =========================
# GRÁFICO 1
# =========================
st.header('Média de Temperatura por Ambiente (Filtrado)')
fig1 = px.bar(df_filtered, x='room_id', y='avg_temp', color='avg_temp')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# =========================
# GRÁFICO 2
# =========================
st.header('Leituras por Hora')
fig2 = px.line(df_hora, x='hora', y='total_leituras', markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# GRÁFICO 3
# =========================
st.header('Temperatura Máxima e Mínima por Dia')
fig3 = px.line(df_temp, x='data', y=['temp_max', 'temp_min'], markers=True)
st.plotly_chart(fig3, use_container_width=True)