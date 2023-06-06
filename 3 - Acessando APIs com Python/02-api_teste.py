import requests
import mysql.connector
from datetime import datetime
    
# URL da API
url = "https://odds.p.rapidapi.com/v4/sports/soccer_brazil_campeonato/scores?daysFrom=3"


# Cabeçalhos da solicitação
headers = {
	"X-RapidAPI-Key": "28a16d2fd8msh32657b05ce9aae9p1121dajsndc74229b9558",
	"X-RapidAPI-Host": "odds.p.rapidapi.com"
}

# Conectar ao banco de dados MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="user_api",
    password="123@456",
    database="pocker_bet"
)

# Verificar se a conexão com o banco de dados foi bem-sucedida
if cnx.is_connected():
    # Criar cursor para executar consultas SQL
    cursor = cnx.cursor()

    # Realizar solicitação GET à API
    response = requests.get(url, headers=headers)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Extrair dados do JSON de resposta
        data = response.json()

        # Processar as partidas e inserir informações na tabela
        for partida in data:
            # Verificar se a partida está completa (completed é igual a True)
            if partida.get("completed") and partida["completed"] == True:
                datahora_partida = datetime.strptime(partida["commence_time"],"%Y-%m-%dT%H:%M:%SZ")
                datahora_partida_str = partida["commence_time"]                
                #data_partida = partida["commence_time"].split("T")[0]
                
                # Verificar se a partida ocorre em 2023
                if datahora_partida.year == 2023:
                    id_api = partida ["id"]
                    data_partida = datahora_partida.date()
                    time_casa = partida["home_team"]
                    time_fora = partida["away_team"]
                    gols_time_casa = None
                    gols_time_fora = None

                # Verificar se os dados de gols estão disponíveis
                if partida["scores"]:
                    for score in partida["scores"]:
                        if score["name"] == time_casa:
                            gols_time_casa = int(score["score"])
                        else:
                            gols_time_fora = int(score["score"])
       
                # Inserir dados na tabela
                insert_query = """
                INSERT INTO partidas_brasileirao_serie_a_2023 (id_api,datahora_partida, data_partida, time_casa, time_fora, gols_time_casa, gols_time_fora)
                VALUES (%s,%s, %s, %s, %s, %s, %s)
                """
                values = (id_api,datahora_partida, data_partida, time_casa, time_fora, gols_time_casa, gols_time_fora)
                cursor.execute(insert_query, values)

        # Efetivar as alterações no banco de dados
        cnx.commit()

        print("Dados inseridos na tabela com sucesso!")
    else:
        print("Erro na solicitação. Código de status:", response.status_code)

    # Fechar cursor e conexão com o banco de dados
    cursor.close()
    cnx.close()
else:
    print("Erro ao conectar ao banco de dados MySQL.")

