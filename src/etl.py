import pandas as pd
from sqlalchemy import create_engine

# carregar CSV
df = pd.read_csv('../data/iot_telemetry_data.csv')

# limpar nomes de colunas
df.columns = df.columns.str.strip().str.lower()

# renomear colunas problemáticas
df = df.rename(columns={
    'room_id/id': 'room_id',
    'noted_date': 'timestamp',
    'temp': 'temperature',
    'out/in': 'location'
})

# converter data
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')

# remover possíveis valores nulos
df = df.dropna()

# visualizar
print(df.head())
print(df.dtypes)

# conexão com banco
engine = create_engine('postgresql://postgres:1234@localhost:5432/iot_db')

# enviar para o banco
df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

print("Dados inseridos no PostgreSQL com sucesso!")