/*Script resposta a)Quanto de rake foi gerado por cada Geração* de jogadores? */

USE pocker_bet;
SELECT
    CASE
        WHEN data_nascimento BETWEEN '1925-01-01' AND '1940-12-31' THEN 'Veteranos'
        WHEN data_nascimento BETWEEN '1941-01-01' AND '1959-12-31' THEN 'Baby_Boomers'
        WHEN data_nascimento BETWEEN '1960-01-01' AND '1979-12-31' THEN 'Geração_X'
        WHEN data_nascimento BETWEEN '1980-01-01' AND '1995-12-31' THEN 'Geração-Y'
        WHEN data_nascimento BETWEEN '1996-01-01' AND '2010-12-31' THEN 'Geração_Z'
        WHEN data_nascimento >= '2010-01-01' THEN 'Geração_Alpha'
        ELSE 'Outros'
    END AS geracao,
    SUM(rake) AS total_rake
FROM resultado
JOIN clientes ON resultado.clientes_id = clientes.id
GROUP BY geracao;