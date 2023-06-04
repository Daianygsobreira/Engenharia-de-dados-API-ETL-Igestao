/*Criando database*/
Create database Pocker_Bet;

/*Criando tabela Clientes*/
USE pocker_bet;
CREATE TABLE clientes (
    id INT PRIMARY KEY,
    sexo CHAR(1),
    data_nascimento DATE,
    data_cadastro DATETIME,
    cidade VARCHAR(255),
    sigla CHAR(2)
);
/*Criando tabela resultado*/
USE pocker_bet;
CREATE TABLE resultado (
    data_acesso DATE,
    clientes_id INT,
    buyin DECIMAL(10, 2),
    rake DECIMAL(10, 2),
    winning DECIMAL(10, 2)
);

