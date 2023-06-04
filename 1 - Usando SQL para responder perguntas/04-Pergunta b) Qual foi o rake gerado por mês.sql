/*Script resposta b)Qual foi o rake gerado por mês? */

USE pocker_bet;
SELECT
    DATE_FORMAT(data_acesso, '%Y-%m') AS mes,
    SUM(rake) AS total_rake
FROM resultado
GROUP BY mes;