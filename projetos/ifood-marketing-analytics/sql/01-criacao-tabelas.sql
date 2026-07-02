-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 01-cria-caotabelas.sql
-- Objetivo: Criar a tabela principal do projeto iFood
-- Autor: Alexander Albuquerque
-- ============================================================

CREATE TABLE IF NOT EXISTS clientes_ifood (
    id_cliente INT PRIMARY KEY,
    ano_nascimento INT,
    escolaridade VARCHAR(100),
    estado_civil VARCHAR(100),
    renda DECIMAL(12,2),
    qtd_criancas_casa INT,
    qtd_adolescentes_casa INT,
    data_cadastro DATE,
    dias_desde_ultima_compra INT,

    gasto_vinhos DECIMAL(12,2),
    gasto_frutas DECIMAL(12,2),
    gasto_carnes DECIMAL(12,2),
    gasto_peixes DECIMAL(12,2),
    gasto_doces DECIMAL(12,2),
    gasto_produtos_gold DECIMAL(12,2),

    compras_com_desconto INT,
    compras_web INT,
    compras_catalogo INT,
    compras_loja INT,
    visitas_web_mes INT,

    campanha_1 INT,
    campanha_2 INT,
    campanha_3 INT,
    campanha_4 INT,
    campanha_5 INT,
    resposta_campanha_final INT,
    reclamacao INT
);
