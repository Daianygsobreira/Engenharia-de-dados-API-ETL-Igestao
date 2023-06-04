use pocker_bet;
CREATE TABLE IF NOT EXISTS partidas_brasileirao_serie_a_2023 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_api varchar (500),
    datahora_partida DATETIME,
    data_partida DATE,
    time_casa VARCHAR(100),
    time_fora VARCHAR(100),
    gols_time_casa INT,
    gols_time_fora INT
);