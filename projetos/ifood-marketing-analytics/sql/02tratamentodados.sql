-- ============================================================
-- Projeto: iFood Marketing Analytics
-- Arquivo: 02-tratamento-dados.sql
-- Objetivo: Criar uma visão tratada da base de clientes
-- Autor: Alexander Albuquerque
-- ============================================================

CREATE VIEW vw_clientes_ifood_tratado AS
SELECT
    id_cliente,
    ano_nascimento,
    EXTRACT(YEAR FROM CURRENT_DATE) - ano_nascimento AS idade,
    escolaridade,
    estado_civil,
    renda,

    qtd_criancas_casa,
    qtd_adolescentes_casa,
    qtd_criancas_casa + qtd_adolescentes_casa AS total_dependentes,

    data_cadastro,
    dias_desde_ultima_compra,

    gasto_vinhos,
    gasto_frutas,
    gasto_carnes,
    gasto_peixes,
    gasto_doces,
    gasto_produtos_gold,

    gasto_vinhos
    + gasto_frutas
    + gasto_carnes
    + gasto_peixes
    + gasto_doces
    + gasto_produtos_gold AS gasto_total,

    compras_com_desconto,
    compras_web,
    compras_catalogo,
    compras_loja,
    compras_web + compras_catalogo + compras_loja AS total_compras,

    visitas_web_mes,

    campanha_1,
    campanha_2,
    campanha_3,
    campanha_4,
    campanha_5,
    resposta_campanha_final,
    reclamacao

FROM clientes_ifood
WHERE renda IS NOT NULL;
