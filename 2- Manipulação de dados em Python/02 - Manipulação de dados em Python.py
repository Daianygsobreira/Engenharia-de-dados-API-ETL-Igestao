import pandas as pd
import mysql.connector

# Configurações de conexão ao banco de dados de origem
config_origin = {
    'user': 'a4f2b49a_padawan',
    'password': 'KaratFlanksUgliedSpinal',
    'host': '40b8f30251.nxcli.io',
    'port': 3306,
    'database': 'a4f2b49a_sample_database'
}

# Configurações de conexão ao banco de dados de destino (local)
config_destination = {
    'user': 'user_api',
    'password': '123@456',
    'host': 'localhost',
    'port': 3306,
    'database': 'pocker_bet'
}

# Função para consolidar os dados
def consolidate_data(df):
    consolidated_df = df.groupby(['mes']).agg(
        rake=('rake', 'sum'),
        jogadores=('clientes_id', 'nunique'),
        rake_cash_game=('rake', lambda x: x[df['modalidade'] == 'Cash Game'].sum()),
        rake_torneio=('rake', lambda x: x[df['modalidade'] == 'Torneio'].sum()),
        jogadores_cash_game=('clientes_id', lambda x: x[df['modalidade'] == 'Cash Game'].nunique()),
        jogadores_torneio=('clientes_id', lambda x: x[df['modalidade'] == 'Torneio'].nunique())
    ).reset_index()
    return consolidated_df

# Conectar ao banco de dados de origem
cnx_origin = mysql.connector.connect(**config_origin)

# Ler os dados da tabela raw_data
query = "SELECT * FROM raw_data"
df = pd.read_sql_query(query, cnx_origin)

# Converter a coluna 'datahora_acesso' para o formato correto
df['datahora_acesso'] = pd.to_datetime(df['datahora_acesso'], errors='coerce')

# Definir o formato desejado para as datas
#df['datahora_acesso'] = df['datahora_acesso'].dt.strftime("%Y-%m-%d")

# Converter a coluna 'datahora_acesso' para o tipo de dado datetimelike
df['datahora_acesso'] = pd.to_datetime(df['datahora_acesso'], errors='coerce')

# Verificar se a conversão foi bem-sucedida
if pd.api.types.is_datetime64_any_dtype(df['datahora_acesso']):
    # Extrair o mês da coluna 'datahora_acesso'
    df['mes'] = df['datahora_acesso'].dt.to_period('M')
    # Converter o tipo de dado Period para string
    df['mes'] = df['mes'].dt.strftime('%Y-%m-01')
    

# Consolidar os dados
    consolidated_df = consolidate_data(df)

# Conectar ao banco de dados de destino
    cnx_destination = mysql.connector.connect(**config_destination)

# Inserir os dados consolidados na tabela existente
    insert_query = "INSERT INTO tabela_consolidada (mes, rake, jogadores, rake_cash_game, rake_torneio, jogadores_cash_game, jogadores_torneio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = consolidated_df.values.tolist()
    cursor = cnx_destination.cursor()
    cursor.executemany(insert_query, values)

# Efetivar as alterações no banco de dados de destino
    cnx_destination.commit()

# Fechar as conexões com os bancos de dados
    cnx_origin.close()
    cnx_destination.close()

    print("Dados consolidados e salvos na tabela 'tabela_consolidada' com sucesso!")
else:
    print("Erro na conversão da coluna 'datahora_acesso' para o tipo de dado datetimelike.")

