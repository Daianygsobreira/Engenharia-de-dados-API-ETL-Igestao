
/*Script resposta c)Qual sexo tem uma maior proporção de ganhadores?*/

USE pocker_bet;
SELECT
    sexo,
    COUNT(*) AS total_clientes,
    COUNT(CASE WHEN winning > 0 THEN 1 END) AS total_ganhadores,
    COUNT(CASE WHEN winning > 0 THEN 1 END) / COUNT(*) AS proporcao_ganhadores
FROM clientes
JOIN resultado ON clientes.id = resultado.clientes_id
GROUP BY sexo
ORDER BY proporcao_ganhadores DESC;